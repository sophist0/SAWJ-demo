#!/usr/bin/env python

import numpy as np
import os

def main():

	fnames = os.listdir('.')

	data = []
	for f in fnames:
		f2 = f.split('.')
		l = len(f2)
		if f2[l-1] == "npy":
			tmp = np.load(f)
			print
			print tmp[0]
			for x in range(len(tmp)):
				data.append(tmp[x])

	np.save('imdb_full',data)

if __name__=='__main__':

	main()
