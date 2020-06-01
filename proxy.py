from urllib.request import ProxyHandler,build_opener
from bs4 import BeautifulSoup

proxy = ProxyHandler({'https' : 'https://127.0.0.1:1080'})
opener = build_opener(proxy)
