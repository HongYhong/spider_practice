import proxy
from urllib.parse import urlparse
import re
import datetime
import random
import os
import sys
from bs4 import BeautifulSoup
from urllib.error import HTTPError,URLError


def getExternalLinks(excludeUrl,bs):
    externalLinks = []
    for link in bs.find_all('a',href = re.compile("^(www|http|https)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'].startswith('www'):
            link.attrs['href'] = 'http://' + link.attrs['href']
        if link.attrs['href'] not in externalLinks:
            externalLinks.append(link.attrs['href'])
#    print(externalLinks)
    return externalLinks

def getInternalLinks(includeUrl,bs,path):
    internalLinks = []
    print('includeUrl is ' + includeUrl)
    print('path is ' + path)
    trimed_path = os.path.dirname(os.path.dirname(path))
    for link in bs.find_all('a',href = re.compile('^(/|\.\.|\.)|'+includeUrl+'.*')):
        if link.attrs['href'].startswith('//'):
            print('process 1:   ' + link.attrs['href'])
            link.attrs['href'] = link.attrs['href'].replace('//','https://')
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link['href'])
        elif link.attrs['href'].startswith('/'):
            print('process 2:   ' + link.attrs['href'])
            link.attrs['href'] = includeUrl + link.attrs['href']
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link['href'])
        elif link.attrs['href'].startswith('..'):
            print('process 3:   ' + link.attrs['href'])
            print('trimed path is '+ trimed_path)
            link.attrs['href'] = link.attrs['href'].replace('^(../)',includeUrl + trimed_path)
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
        elif link.attrs['href'].startswith('.'):
            print('process 4:   ' + link.attrs['href'])
            link.attrs['href'] = link.attrs['href'].replace('.',includeUrl)
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
        else:
            print('process 5:   ' + link.attrs['href'])
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    print(internalLinks)
    return internalLinks

random.seed(datetime.datetime.now())

def getRandomExternalLinks(url):
    try:
        html =proxy.opener.open(url)
    except HTTPError as e:
        print(e)
    try:
        bs = BeautifulSoup(html,'html.parser')
    except AttributeError as e:
        print(e)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    try:
        externalLinks = getExternalLinks(urlparse(url).netloc,bs)
        if (len(externalLinks) == 0):
            print('no external links found! try internal links....')
            domain = urlparse(url).scheme + '://' + urlparse(url).netloc
            path = urlparse(url).path
            internalLinks = getInternalLinks(domain,bs,path)
            if (len(internalLinks) == 0):
                print('no internal links found! exit!')
                return None
            return internalLinks[random.randint(0,len(internalLinks) - 1)]
        else:
            return externalLinks[random.randint(0,len(externalLinks) - 1)]
    except :
        print('something happens during process of getting external links...')

def followExternalLinksOnly(url):
    link = getRandomExternalLinks(url)
    if link == None:
        sys.exit()
    print(link)
    followExternalLinksOnly(link)

def getAllExternalLinks(url):
    try:
        html =proxy.opener.open(url)
    except HTTPError as e:
        print(e)
    try:
        bs = BeautifulSoup(html,'html.parser')
    except AttributeError as e:
        print(e)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    try:
        externalLinks = getExternalLinks(urlparse(url).netloc,bs)
    except:
        pass
    if len(externalLinks) == 0:
        print('enter link: ',url)
        print('no external links found!')
        sys.exit()
    print('enter link: ' + url)
    print('All external links: ', externalLinks)
    print('-------------------------------------------------------------------')
    link = externalLinks[random.randint(0,len(externalLinks) - 1)]
    getAllExternalLinks(link)

def getAllInternalLinks(url):
    try:
        html =proxy.opener.open(url)
    except HTTPError as e:
        print(e)
    try:
        bs = BeautifulSoup(html,'html.parser')
    except AttributeError as e:
        print(e)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    try:
        domain = urlparse(url).scheme + '://' + urlparse(url).netloc
        path = urlparse(url).path
        internalLinks = getInternalLinks(domain,bs,path)
    except:
        pass
    if len(internalLinks) == 0:
        print('no internal links found!')
        sys.exit()
    print('enter link: ' + url)
    print('All internal links: ',internalLinks)
    print('-------------------------------------------------------------------')
    link = internalLinks[random.randint(0,len(internalLinks) - 1)]
    getAllExternalLinks(link)

#followExternalLinksOnly('https://www.google.com')
getAllExternalLinks('https://en.wikipedia.org/wiki/Kevin_Bacon')