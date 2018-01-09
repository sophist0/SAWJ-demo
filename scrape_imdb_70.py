#!/usr/bin/env python

from lxml import html
import requests
from selenium import webdriver
import copy
import numpy as np
import re

def main():

	collect_data = []
	driver = webdriver.Chrome()
	t_page = 101
	for page in range(1,40):

		########################################
		# loop over title result pages
		########################################

		url = "http://www.imdb.com/search/title?count=100&num_votes=1000,&production_status=released&release_date=1970-01-01,1990-12-31&title_type=feature&page="+str(page)	
		driver.get(url)
		tree = html.fromstring(driver.page_source)

		for x in range(1,t_page):

			print "##############################################"

			title = tree.xpath('//*[@id="main"]/div/div/div[3]/div['+str(x)+']/div[3]/h3/a/text()')

			if title != []:

				print
				print "title: ", title
				print

				stars = []
				direct = []
				l_num = 1
				name = tree.xpath('//*[@id="main"]/div/div/div[3]/div['+str(x)+']/div[3]/p[3]/a['+str(l_num)+']/text()')
				while name != []:

					link = tree.xpath('//*[@id="main"]/div/div/div[3]/div['+str(x)+']/div[3]/p[3]/a['+str(l_num)+']/@href')
					plink = parse_link(link)
					if plink == 'director':
						direct.append(name)
					else:
						stars.append(name) 

					l_num += 1
					name = tree.xpath('//*[@id="main"]/div/div/div[3]/div['+str(x)+']/div[3]/p[3]/a['+str(l_num)+']/text()')

				votes = tree.xpath('//*[@id="main"]/div/div/div[3]/div['+str(x)+']/div[3]/p[4]/span[2]/text()')
				rating = tree.xpath('//*[@id="main"]/div/div/div[3]/div['+str(x)+']/div[3]/div/div[1]/strong/text()')
				metascore = tree.xpath('//*[@id="main"]/div/div/div[3]/div['+str(x)+']/div[3]/div/div[3]/span/text()')
				print "rating: ",rating
				print "metascore: ",metascore
				print "votes: ", votes
				print "directors: ", direct
				print "stars: ", stars

				collect_data.append([title,direct,stars,votes,rating,metascore])

	driver.quit()
	collect_data = np.asarray(collect_data)
	np.save('data/imdb_data_70.p',collect_data)

def parse_link(link):

	pattern = 'adv_li_st'
	match = re.search(r'adv\_li\_st', link[0])

	if match:
		return "star"
	else:
		return "director"	
		
if __name__=='__main__':

	main()
