#Crawling whole site in wiki

import proxy
from bs4 import BeautifulSoup
from urllib.error import URLError,HTTPError
import re
import sys

pages = set()
def getLinks(articleURL):
	try:
		html = proxy.opener.open(articleURL).read()
	except HTTPError as e:
		print(e)
	try:
		bs = BeautifulSoup(html,'html.parser')
	except AttributeError as e:
		print(e)
	try:
		print (bs.h1.get_text())
		print (bs.find('div',{'id':'mw-content-text'}).find_all('p')[1].get_text())
	except:
		print('miss some attributes!')
	try:
		new_pages = bs.find('div',{'id' : 'bodyContent'}).find_all('a', {'href' : re.compile('^(/wiki/)((?!:).)*$')})
		for page in new_pages:
			new_page = 'https://en.wikipedia.org{}'.format(page.attrs['href'])
			if new_page not in pages:
				print('-'*20)
				print(new_page)
				pages.add(new_page)
				getLinks(new_page)
	except:
		print('Tag is not found!')

getLinks(sys.argv[1])
