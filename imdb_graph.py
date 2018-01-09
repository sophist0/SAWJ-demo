#!/usr/bin/env python

import numpy as np
import igraph as ig
import pickle_imdb_graph as pg

def main():

	data = np.load('imdb_full.npy')

	stars_added = []
	g = ig.Graph()
	n_vert = 0
	print
	print "Adding vertices"
	print
	for x in range(len(data)):

		title = data[x][0][0]

		dir_data = []
		if data[x][1] != 0:
			for y in range(len(data[x][1])):
				dir_data = dir_data + data[x][1][y]

		star_data = []
		if data[x][2] != 0:
			for y in range(len(data[x][2])):
				star_data = star_data + data[x][2][y]

		if data[x][3] != 0:
			t = data[x][3][0].split(',')
			votes = ""
			for y in range(len(t)):
				votes = votes + t[y]
		votes = int(votes)

		# if no value set scores to -1
		rating = -1
		if data[x][4] != []:
			rating = float(data[x][4][0])

		metascore = -1
		if data[x][5] != []:
			metascore = float(data[x][5][0])

		# add title node	
		g.add_vertices(1)
		g.vs[n_vert]['type'] = 'film'
		g.vs[n_vert]['title'] = title
		g.vs[n_vert]['directors'] = dir_data
		g.vs[n_vert]['stars'] = star_data
		g.vs[n_vert]['votes'] = votes
		g.vs[n_vert]['rating'] = rating
		g.vs[n_vert]['metascore'] = metascore	

		# add star vertices only if the star vertex does not already exist
		v_add = 0
		for y in range(len(g.vs[n_vert]['stars'])):
			new_star = True
			for el in stars_added:
				if (el == g.vs[n_vert]['stars'][y]):
					new_star = False
					break

			if new_star == True:
				g.add_vertices(1)
				v_add += 1
				g.vs[n_vert+v_add]['type'] = 'star'
				g.vs[n_vert+v_add]['name'] = g.vs[n_vert]['stars'][y]
				stars_added.append(g.vs[n_vert]['stars'][y])

		n_vert += (1 + v_add)
		
	# Need a second pass to add edges
	print
	print "n_vert: ",n_vert
	print
	print "Adding edges"
	print
	e = 1
	for x in range(len(g.vs)):
		if (g.vs[x]['type']=='film'):
			for k in range(len(g.vs[x]['stars'])):
				for y in range(len(g.vs)):
					if (g.vs[y]['type'] == 'star') and (g.vs[x]['stars'][k] == g.vs[y]['name']):
						g.add_edge(x,y)
						if (e % 1000) == 0:
							print "node: "+str(x)+" of "+str(len(g.vs))+", edge count: "+str(e)
						e += 1
	print
	print "Finished adding edges"
	print
	pg.pickle_graph(g,"imdb_full")
	
if __name__=='__main__':

	main()
