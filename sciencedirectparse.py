import re
from bs4 import BeautifulSoup
import os
import itertools
import cfscrape


scraper = cfscrape.create_scraper()
f = open('articlesabsctracts.csv', 'w')

month = 67
while month > 1:
	month = month - 1
	print ("Month ", month) 
	link = "http://top25.sciencedirect.com/archive/" + str(month)
	print (link)
	r = scraper.get(link).text
	soup = BeautifulSoup(r)
	articles = soup.findAll('a', { "target" : "_blank" })[1:-2]
	for i in range(len(articles)-1):
		title = articles[i].get_text()
		title = re.sub(';', ',', title)
		link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(articles[i]))[0]
		pii =re.sub('http://www.sciencedirect.com/science/article/pii/','',link)
		link = 'https://api.elsevier.com/content/article/pii/[{:s}]'.format(pii)
		r = scraper.get(link).text
		abstract = ''
		try:
			abstract = re.findall('dc:description.*?dc:description', r)[0][15:-16]
			abstract = re.sub(';', ',', abstract)
			abstract = abstract.encode('utf-8')
			if abstract.startswith('Absctract'):
				abstract = re.sub('Absctract','', abstract)
			elif abstract.startswith('Summary'):
				abstract = re.sub('Summary','', abstract)
			title = title.encode('utf-8')
			print (title)
			print (link)
			f.write(title + ';' + link + ';' + pii + ';' + abstract + '\n')

		except:
			pass
