#!/usr/bin/env python

import random
import numpy as np
import igraph as ig
import argparse
import math
import os
import copy
import cPickle as pickle
import pickle_imdb_graph as p_imdb
from terminaltables import AsciiTable

def main():
	
	# graph to search
        graph_file = 'imdb_full.p'

	# load pickled object 
	# T0DO make graph edge list
	[graph, a_deg, a_votes] = p_imdb.load_pickled_graph(graph_file)

	# number of results displayed
	n = 2

	# number of samples/iterations of each sampling algorithm
	n_samples = 50

	# table 1 for degree results
	title1 = "degree"
	#tb_data1 = [['','film 1','film 2','film 3','star 1','star 2', 'star 3','v-nodes','e-nodes']]
	tb_data1 = [['']]
	for x in range(n):
		tb_data1[0].append('film'+str(x+1))
	for x in range(n):
		tb_data1[0].append('star'+str(x+1))
	tb_data1[0].append('v-nodes')
	tb_data1[0].append('e-nodes')


	# table 2 for vote results
	title2 = "vote"
	tb_data2 = [['']]
	for x in range(n):
		tb_data2[0].append('film'+str(x+1))
	for x in range(n):
		tb_data2[0].append('star'+str(x+1))
	tb_data2[0].append('v-nodes')
	tb_data2[0].append('e-nodes')


	#print "######################################################################"
	#print "Exhaustive"
	#print "######################################################################"

	deg_type = 'degree'
	data = getMaxes(graph,n,deg_type)	
	#printMaxes(data,n,deg_type)		
	rtmp = add_data(data,'Exhaustive',len(graph.vs),len(graph.vs))
	tb_data1.append(rtmp)	
	#print "Exhaustive Nodes Examined: ", len(graph.vs)

	deg_type = 'vote_w'
	data = getMaxes(graph,n,deg_type)	
	#printMaxes(data,n,deg_type)
	rtmp = add_data(data,'Exhaustive',len(graph.vs),len(graph.vs))
	tb_data2.append(rtmp)	
	#print "Exhaustive Nodes Examined: ", len(graph.vs)
	#print

	#print "######################################################################"
	#print "Star Sample"
	#print "######################################################################"

	deg_type = 'degree'
	tmp = star_sample(graph, n_samples, n, deg_type)
	data = [tmp[0],tmp[1]]
	#printMaxes(data,n,deg_type)
	#print "Visited Nodes: ", tmp[2]
	#print "Examined Nodes: ", tmp[3]
	rtmp = add_data(data,'Star Sample',tmp[2],tmp[3])
	tb_data1.append(rtmp)	
	#print

	deg_type = 'vote_w'
	tmp = star_sample(graph, n_samples, n, deg_type)
	data = [tmp[0],tmp[1]]
	#printMaxes(data,n,deg_type)
	#print "Visited Nodes: ", tmp[2]
	#print "Examined Nodes: ", tmp[3]
	#print
	rtmp = add_data(data,'Star Sample',tmp[2],tmp[3])
	tb_data2.append(rtmp)	

	#print "####################################################################################################################"
	#print "SAWJ (can examine more nodes then exhaustive search in dense graphs given nodes in multiple node neighborhoods FIX?)"
	#print "####################################################################################################################"

	# while actual assortativity of a_deg and a_votes is slightly disassortative, it is assumed the high degree movies have high degree actors and therefore the nodes be are interested in are associative

	# assortativity numbers actual and used
	alpha = 1
	print
	print "########################################"
	print "a_deg: ", a_deg
	print "a_votes: ", a_votes
	print "alpha: ", alpha
	print "########################################"
	print
	n_walk = 50
	maxSteps = pow(10,7)

	####################################################################

	jprob = 0.0

	deg_type = 'degree'
	tmp = unifiedWalk(graph, maxSteps, alpha, jprob, deg_type, n, n_walk)
	data = [tmp[0],tmp[1]]
	#printMaxes(data,n,deg_type)
	#print "Visited Nodes: ", tmp[2]
	#print "Examined Nodes: ", tmp[3]
	#print
	rtmp = add_data(data,'SAWJ b=0',tmp[2],tmp[3])
	tb_data1.append(rtmp)	

	deg_type = 'vote_w'
	tmp = unifiedWalk(graph, maxSteps, alpha, jprob, deg_type, n, n_walk)
	data = [tmp[0],tmp[1]]
	#printMaxes(data,n,deg_type)
	#print "Visited Nodes: ", tmp[2]
	#print "Examined Nodes: ", tmp[3]
	#print
	rtmp = add_data(data,'SAWJ b=0',tmp[2],tmp[3])
	tb_data2.append(rtmp)	

	####################################################################

	jprob = 0.5

	deg_type = 'degree'
	tmp = unifiedWalk(graph, maxSteps, alpha, jprob, deg_type, n, n_walk)
	data = [tmp[0],tmp[1]]
	#printMaxes(data,n,deg_type)
	#print "Visited Nodes: ", tmp[2]
	#print "Examined Nodes: ", tmp[3]
	#print
	rtmp = add_data(data,'SAWJ b=0.5',tmp[2],tmp[3])
	tb_data1.append(rtmp)	

	deg_type = 'vote_w'
	tmp = unifiedWalk(graph, maxSteps, alpha, jprob, deg_type, n, n_walk)
	data = [tmp[0],tmp[1]]
	#printMaxes(data,n,deg_type)
	#print "Visited Nodes: ", tmp[2]
	#print "Examined Nodes: ", tmp[3]
	#print
	rtmp = add_data(data,'SAWJ b=0.5',tmp[2],tmp[3])
	tb_data2.append(rtmp)	

	####################################################################

	jprob = 1

	deg_type = 'degree'
	tmp = unifiedWalk(graph, maxSteps, alpha, jprob, deg_type, n, n_walk)
	data = [tmp[0],tmp[1]]
	#printMaxes(data,n,deg_type)
	#print "Visited Nodes: ", tmp[2]
	#print "Examined Nodes: ", tmp[3]
	#print
	rtmp = add_data(data,'SAWJ b=1',tmp[2],tmp[3])
	tb_data1.append(rtmp)	

	deg_type = 'vote_w'
	tmp = unifiedWalk(graph, maxSteps, alpha, jprob, deg_type, n, n_walk)
	data = [tmp[0],tmp[1]]
	#printMaxes(data,n,deg_type)
	#print "Visited Nodes: ", tmp[2]
	#print "Examined Nodes: ", tmp[3]
	#print
	rtmp = add_data(data,'SAWJ b=1',tmp[2],tmp[3])
	tb_data2.append(rtmp)	

	####################################################################
	# print the tables
	####################################################################
	print
	tb1 = AsciiTable(tb_data1,title1)
	tb2 = AsciiTable(tb_data2,title2)

	print tb1.table
	print
	print tb2.table
	print

def unifiedWalk(graph, maxSteps, alpha, jprob, dtype, n, n_walk):

	#############################################################
	# Walking the actual graph degrees not the user ratings
	#############################################################

	# n_walk is the number of nodes that can be walked

	max_film = [0 for x in range(n)]
	max_star = [0 for x in range(n)]
	id_film = [-1 for x in range(n)]
	id_star = [-1 for x in range(n)]

        # choosing start vertex Uniformly at random
	v = random.choice(graph.vs)
           
        visited_nodes = []
	# index 0 is the film, index 1 is the brewery
	names = [[],[]]
	count = 0
	n_examined = 1
        while count < n_walk:
		count += 1

       		visited_nodes.append(v.index)
                neighborhood = v.neighbors()

                # check if in the neighborhood of a max degree node
                # only matters for alpha < 0
                flag = 0 

                for nn in neighborhood:
			n_examined += 1
			el = gen_deg(nn, dtype)
                        if (nn['type']=='film') and (el > max_film[n-1]) and (id_film.count(nn.index)==0):
				[max_film,id_film] = add_larger(max_film,id_film,el,nn.index)

                        if (nn['type']=='star') and (el > max_star[n-1]) and (id_star.count(nn.index)==0):
				[max_star,id_star] = add_larger(max_star,id_star,el,nn.index)
 
                # check if there are unvisited nodes in the neighborhood
                uvisit = False
                for nn in neighborhood:
                        # returns false if there exists an unvisited node
                        uvisit = check_visited(nn,visited_nodes)
                        if uvisit == False:
                                break

                if (uvisit == False) and (neighborhood != []):
                        # check if at a strict local maxima or minima, returns false if not a strict or non-max !!!! max/min
                        # in this case there are no nodes in its neighborhood of strictly greater degree
                        if alpha >= 0:
                                lm = check_lmax_fix(v,neighborhood,visited_nodes,dtype)
                        else:
                                lm = check_lmin_fix(v,neighborhood,visited_nodes,dtype)

                        # Goto max
                        if lm == 0 and alpha >= 0:
                                n_index = get_NodeIndex(neighborhood)
                                v = moveToMax(neighborhood,n_index,visited_nodes,graph,dtype) 
                        # Goto min
                        elif lm == 0:
                                n_index = get_NodeIndex(neighborhood)
                                v = moveToMin(neighborhood,n_index,visited_nodes,graph,dtype)  
                        # Goto jump cases
                        else:
                                r = random.random()
                                if r < jprob:
                                        # select an unvisited node uniformly at random from G
                                        v = jump(graph,visited_nodes)

                                else:
                                        # select an unvisited node uniformly at random from v's neighborhood
                                        if alpha >= 0:
                                                n_index = get_NodeIndex(neighborhood)
                                                v = moveToMax(neighborhood,n_index,visited_nodes,graph,dtype)
                                        else:
                                                n_index = get_NodeIndex(neighborhood)
                                                v = moveToMin(neighborhood,n_index,visited_nodes,graph,dtype)
                else:
                        v = jump(graph,visited_nodes)

	n_film = []
	n_star = []
	for x in range(n):
		n_film.append(graph.vs[id_film[x]]['title'])		
		n_star.append(graph.vs[id_star[x]]['name'])		

	data_film = [max_film,n_film]
	data_star = [max_star,n_star]

	return [data_film, data_star, len(visited_nodes), n_examined]

def printMaxes(data,n,dtype):

	print
	print "##########################"
	print "dtype: ", dtype
	print "##########################"
	print "Films"
	for x in range(n):
		print str(data[0][0][x]) + ': ' + data[0][1][x]

	print
	print "Stars"
	for x in range(n):
		print str(data[1][0][x]) + ': ' + data[1][1][x]
	print

def add_data(data,algName,vnodes,enodes):

	rtmp = [algName]
	for x in range(len(data[0][0])):
		rtmp.append(str(data[0][0][x]) + ': ' + data[0][1][x])
	for x in range(len(data[1][0])):
		rtmp.append(str(data[1][0][x]) + ': ' + data[1][1][x])
	rtmp.append(vnodes)
	rtmp.append(enodes)

	return rtmp

def getMaxes(graph,n,dtype):

	max_star = [0 for x in range(n)]
	id_star = [-1 for x in range(n)]

	max_film = [0 for x in range(n)]
	id_film = [-1 for x in range(n)]

	for x in range(len(graph.vs)):
			
		el = gen_deg(graph.vs[x], dtype)
		if (graph.vs[x]['type'] == 'film') and (gen_deg(graph.vs[x], dtype) > max_film[n-1]):
			[max_film,id_film] = add_larger(max_film,id_film,el,x)

		if (graph.vs[x]['type'] == 'star') and (gen_deg(graph.vs[x], dtype) > max_star[n-1]):
			[max_star,id_star] = add_larger(max_star,id_star,el,x)

	n_film = []
	n_star = []
	for x in range(n):
		n_film.append(graph.vs[id_film[x]]['title'])		
		n_star.append(graph.vs[id_star[x]]['name'])		

	data_film = [max_film,n_film]
	data_star = [max_star,n_star]

	return [data_film, data_star]

def add_larger(el_vec,id_vec,el,el_id):
	
	n = len(el_vec)
	idx = n-1
	added = False
	for y in range(len(el_vec)):
		if el_vec[idx-y] > el:
			el_vec[idx-y+1:n] = [el] + el_vec[idx-y+1:n-1]
			id_vec[idx-y+1:n] = [el_id] + id_vec[idx-y+1:n-1]
			added = True
			break
	if added == False:
		el_vec = [el] + el_vec[0:n-1]
		id_vec = [el_id] + id_vec[0:n-1]

	return [el_vec, id_vec]

def gen_deg(v, dtype):
	# function to get generic node degree

	d = -1
	if dtype == 'degree':
		d = v.degree()
	elif dtype == 'vote_w':
		d = v['vote_w']

	return d

def remove_visited(n_index,visited_nodes):

        nTemp = copy.deepcopy(n_index)

        # remove visited nodes from neighborhood
        # could be done in visited nodes check
        for nn in n_index:
                visited = False
                visited = check_visited_2(nn,visited_nodes)
                if visited == True:
                        nTemp.remove(nn)

        return nTemp

def moveToMax(neighborhood, n_index ,visited_nodes, graph, dtype):

        # remove visited nodes from neighborhood
        # could be done in visited nodes check
        nTemp = remove_visited(n_index,visited_nodes)

	if len(nTemp) > 0:

		# Find max degree in the neighborhood   
		n_dmax = 0
		for o in neighborhood:
			for i in nTemp:
				if (i == o.index) and (gen_deg(o, dtype) > n_dmax):
					n_dmax = gen_deg(o, dtype)
					break

		# collect max neighboring nodes
		n_max = []
		for o in neighborhood:
			for i in nTemp:
				if (i == o.index) and gen_deg(o, dtype) == n_dmax:
					n_max.append(o)

		v = random.choice(n_max)

	else:
		v = jump(graph,visited_nodes)

        return v

def moveToMin(neighborhood, n_index, visited_nodes, graph, dtype):

        # remove visited nodes from neighborhood
        # could be done in visited nodes check
        nTemp = remove_visited(n_index,visited_nodes)

        # Find min degree in the neighborhood  
        # But if in the neighborhood of a max degree node move to it instead 
        n_dmin = 1000000
        for o in neighborhood:
                for i in nTemp:
                        if (i == o.index) and (gen_deg(o, dtype) < n_dmin) and (gen_deg(o, dtype) > 1):
                                n_dmin = gen_deg(o, dtype)

        # jump if neighbors are all degree 1 nodes
        if n_dmin == 1000000:
                v = jump(graph,visited_nodes)
        else:
                # collect max neighboring nodes
                n_min = []
                for o in neighborhood:
                        for i in nTemp:
                                if (i == o.index) and (gen_deg(o, dtype) == n_dmin):
                                        n_min.append(o)

                v = random.choice(n_min)
        return v

def get_NodeIndex(nodes):
	# input list of nodes
	n_index = []
	for n in nodes:
		n_index.append(n.index)

	return n_index

def jump(graph,visited_nodes):

	visited = True
	while visited == True:
		v = random.choice(graph.vs)
		visited = check_visited(v,visited_nodes)

	return v

def check_visited(v, visited_nodes):
    
        bad_v = False
        for node in visited_nodes:
                if node == v.index:
                        bad_v = True
                        break
        return bad_v   

def check_visited_2(v, visited_nodes):

	bad_v = False
	for node in visited_nodes:
		if node == v:
			bad_v = True
			break
	return bad_v   

def check_lmax_fix(v,neighbors,visited,dtype):
        # checks if node is a strict or non-strict local max

        n_index = get_NodeIndex(neighbors)
        n_tmp = remove_visited(n_index,visited)

        n_deg = []
        for idx in n_tmp:
                for nn in neighbors:
                        if nn.index == idx:
                                n_deg.append(gen_deg(nn, dtype))


        lm = True
        for el in n_deg:
                if el > gen_deg(v, dtype):
                        lm = False

        return lm

def check_lmin_fix(v,neighbors,visited,dtype):
        # checks if node is a strict of non-strict local min

        n_index = get_NodeIndex(neighbors)
        n_tmp = remove_visited(n_index,visited)

        n_deg = []
        for idx in n_tmp:
                for nn in neighbors:
                        if nn.index == idx:
                                n_deg.append(gen_deg(nn, dtype))

        lm = True
        for el in n_deg:
                # el > 1 to prevent getting stuck when neighbors are degree 1
                if (el < gen_deg(v, dtype)) and (el > 1):
                        lm = False

        return lm

def star_sample(g,max_samples,n,dtype):

	# Star sampling without replacing the sampled cluster

	# max sampled
	m_sampled = 0
	samples = 0
	chosen = []
	max_film = [0 for x in range(n)]
	max_star = [0 for x in range(n)]
	id_film = [-1 for x in range(n)]
	id_star = [-1 for x in range(n)]

	while samples < max_samples:

		samples += 1

		# choose central node
		bad_choice = True
		while bad_choice == True:
			v = random.choice(g.vs)
			v_idx = v.index
			bad_choice = check_chosen(chosen, v_idx)

		chosen.append(v_idx)
		el = gen_deg(v, dtype)
		if (el > max_film[n-1]) and (v['type'] == 'film') and (id_film.count(v.index)==0):
			[max_film,id_film] = add_larger(max_film,id_film,el,v.index)
		
		if (el > max_star[n-1]) and (v['type'] == 'brewery') and (id_star.count(v.index)==0):
			[max_star,id_star] = add_larger(max_star,id_star,el,v.index)	


		if (v.degree() != 0):
			neighbors = v.neighbors()

			# get degrees of neighboring nodes
			for u in neighbors:
				if check_chosen(chosen,u.index) == False:
					chosen.append(u.index)
					
 					el = gen_deg(u, dtype)
                       			if (el > max_film[n-1]) and (u['type'] == 'film') and (id_film.count(u.index)==0):
						[max_film,id_film] = add_larger(max_film,id_film,el,u.index)
					
                       			if (el > max_star[n-1]) and (u['type'] == 'star') and (id_star.count(u.index)==0):
						[max_star,id_star] = add_larger(max_star,id_star,el,u.index)	

	n_film = []
	n_star = []
	for x in range(n):
		n_film.append(g.vs[id_film[x]]['title'])		
		n_star.append(g.vs[id_star[x]]['name'])		

	data_film = [max_film,n_film]
	data_star = [max_star,n_star]

	return [data_film, data_star, samples, len(chosen)]

def check_chosen(chosen,el):

	c = False
	for x in chosen:
		if x == el:
			c = True
			break

	return c			


if __name__ == '__main__':

	main()

