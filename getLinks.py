import proxy
from bs4 import BeautifulSoup
from urllib.error import URLError,HTTPError
import re
import sys
import random
import datetime

random.seed(datetime.datetime.now())

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
		return bs.find('div',{'id' : 'bodyContent'}).find_all('a', {'href' : re.compile('^(/wiki/)((?!:).)*$')})
	except:
		print('Tag is not found!')

links = getLinks(sys.argv[1])

while(len(links) > 0):
	newURL = 'https://en.wikipedia.org{}'.format(links[random.randint(0,len(links)-1)].attrs['href'])
	print(links)
	links = getLinks(newURL)


