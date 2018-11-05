from proxy_getter import get_viable_proxy_list
from proxy_getter import get_html_proxy
from bs4 import BeautifulSoup
import requests
import random
import time
import os

def get_html(url, user_agent, proxy):
	# при выполнении get получаем ответ Response 200. Это означает что все ок.
	r = requests.get(url, timeout = None, proxies = {'': proxy})
	return r.text


def main():
	list_of_viable_proxies = get_viable_proxy_list(get_html_proxy('https://www.ip-adress.com/proxy-list'),10)
	cur_dir = os.path.dirname(__file__)
	useragent_filename = os.path.join(cur_dir, 'useragents.txt')
	list_of_user_agents = open(useragent_filename).read().split('\n')

	# то, что должно быть в цикле
	time.sleep(round(abs(random.gauss(1.5, 1) + random.random()/10 + random.random()/100), 4))
	useragent = {'User-Agent': random.choice(list_of_user_agents)}
	proxy = {'http': random.choice(list_of_viable_proxies)}

	url_gen = "https://yandex.ru/"
	html = get_html(url_gen, useragent, proxy)
	print(html)
	print("\nДанные страницы получены через прокси = ", proxy, '\n', "useragent = ", useragent, '\n')

if __name__ == '__main__':
	main()
