#!/usr/bin/env python

import numpy as np
import cPickle as pickle
import os
import igraph as ig
import math

def pickle_graph(graph,gname):
	# INPUT: iGraph graph object

	# need to add VS attributes
	num_nodes = len(graph.vs)
	num_edges = len(graph.es)

	vs_list = graph.vs.indices
	es_list = []
	for x in range(len(graph.es.indices)):
		es_list.append(graph.es[x].tuple)

	# if attribute does not exist for node saved as []
	vs_types = graph.vs['type']

	vs_names = graph.vs['name'] # only starsa

	vs_titles = graph.vs['title'] # only films
	vs_directors = graph.vs['directors'] # only films
	vs_stars = graph.vs['stars'] # only films
	vs_votes = graph.vs['votes'] # only films
	vs_rating = graph.vs['rating'] # only films
	vs_metascore = graph.vs['metascore'] # only films

	# calculate graph assortativity from node (DEGREE)
	max_deg = graph.maxdegree()
	dseq = graph.vs.degree()
	
	j_mat = calcJointDeg(es_list,dseq,max_deg)
	j_mat = np.asarray(j_mat)
	print
	print "j_mat: ", len(j_mat) 
	print j_mat
	print
	alpha_deg = calc_assort(j_mat)

	# calculate graph assortativity from node (VOTES)
	vseq = [0 for x in range(len(graph.vs))]
	for x in range(len(graph.vs)):
		v = graph.vs[x]
		if v['type'] == 'film':
			vseq[x] = graph.vs[x]['votes']
		else:
			neighbors = v.neighbors()
			n_votes = 0
			for nn in neighbors:
				n_votes += nn['votes']

			vseq[x] = n_votes

	# Since we can't handle a j_mat of 100k+ entries scale entries of v_seq to [1,...,101]
	#vsum = sum(vseq)
	vnorm = max(vseq)
	for x in range(len(vseq)):
		vseq[x] = int(math.ceil((vseq[x]/float(vnorm))*1000))

	max_v = int(max(vseq))
	
	j_mat = calcJointDeg(es_list,vseq,max_v)
	j_mat = np.asarray(j_mat)
	print
	print "max vseq: ", max(vseq)
	print
	print "j_mat: ", len(j_mat) 
	print j_mat
	print
	alpha_votes = calc_assort(j_mat)

	# pickle object
	sg = SavedGraph(num_nodes, num_edges, vs_list, es_list, vs_types, vs_names, vs_titles, vs_directors, vs_stars, vs_votes, vs_rating, vs_metascore, alpha_deg, alpha_votes)

	pickle.dump(sg, open(gname+".p","wb"),-1)

def calcJointDeg(edge_list, deg_seq, max_d):
	# edge_list type is List
 	# deg_seq type is List
	# max_d is int

	# has no zero degree vertices
	jd_mat = [[0 for x in range(max_d)] for y in range(max_d)]

	for x in range(len(edge_list)):
		t = edge_list[x]
		jd_mat[deg_seq[t[0]]-1][deg_seq[t[1]]-1] += 1
		jd_mat[deg_seq[t[1]]-1][deg_seq[t[0]]-1] += 1

	return jd_mat

def calc_assort(M):
	# M is the joint degree matrix, data type numpy array
	# I took this code from a graph library, forget which one

	# degree degree edge counts to probabilities
	M = M/float(M.sum())

	# get number of rows and cols
	nx,ny = M.shape

	# form vectors with these dimensions containing the degree of the nodes minus the connecting edge 
	# from Newmans Def.
	x = np.arange(nx)	# (0 to nx-1)
	y = np.arange(ny)

	# Let a = start node; b = end node of an edge
	# Find the probability distribution of being the degrees in x and y
	a=M.sum(axis=0)
	b=M.sum(axis=1)

	# Var = E[X^2] - (E[X])^2 
	# Note sum(a*x) = the expected value of the start node
	va = (a*x**2).sum() - ((a*x).sum())**2
	vb = (b*x**2).sum() - ((b*x).sum())**2

	# find the joint values of x,y and a,b via matrix multiplication
	xy = np.outer(x,y)
	ab = np.outer(a,b)

	# M = e_{x,y} in Newman's notation or the fraction of all links that connect nodes of degree x and y.
	n = (xy*(M-ab)).sum()

	# denominator is the sqrt of the variances multiplied together
	d = np.sqrt(va*vb)

	print
	print "n: ",n
	print "d: ",d
	print

	r = n/float(d)
	return r

def load_pickled_graph(gname):

	sg = pickle.load(open(gname,"rb"))
	a_deg = sg.a_deg
	a_votes = sg.a_votes

	g = ig.Graph()

	g.add_vertices(len(sg.vs_list))
	g.add_edges(sg.es_list)

	g.vs['type'] = sg.vs_types
	g.vs['name'] = sg.vs_names
	g.vs['title'] = sg.vs_titles
	g.vs['directors'] = sg.vs_directors
	g.vs['stars'] = sg.vs_stars
	g.vs['votes'] = sg.vs_votes
	g.vs['rating'] = sg.vs_rating
	g.vs['metascore'] = sg.vs_metascore


	########################################
	# get vote weight for films and stars
	########################################

	g.vs['vote_w'] = [0 for x in range(len(g.vs))]

	for x in range(len(g.vs)):
		v = g.vs[x]
		if v['type'] == 'film':
			g.vs[x]['vote_w'] = g.vs[x]['votes']
		else:
			neighbors = v.neighbors()
			n_votes = 0
			for nn in neighbors:
				n_votes += nn['votes']

			g.vs[x]['vote_w'] = n_votes

	
	return [g, a_deg, a_votes]
		
class SavedGraph:

	def __init__(self, num_n, num_e, vs_list, es_list, vs_types, vs_names, vs_titles, vs_directors, vs_stars, vs_votes, vs_rating, vs_metascore, alpha_deg, alpha_votes):
		# deg_dist and A_mat are numpy arrays
		self.num_n = num_n # num nodes
		self.num_e = num_e # num edges
		self.a_deg = alpha_deg
		self.a_votes = alpha_votes

		self.vs_list = vs_list
		self.es_list = es_list

		self.vs_types = vs_types
		self.vs_names = vs_names

		self.vs_titles = vs_titles
		self.vs_directors = vs_directors
		self.vs_stars = vs_stars
		self.vs_votes = vs_votes
		self.vs_rating = vs_rating
		self.vs_metascore = vs_metascore
