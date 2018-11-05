import requests
import os
import random
import time
import re

def get_html_txt(url, useragent, proxy):

    r = requests.get(url, headers=useragent, timeout = None, proxies = {'': proxy})
    return r.text

def write_to_file(dir, link, _soup_):

    with open(dir+'/'+'file'+'.txt','a') as f:
        # Ссылка
        f.write('URL: ' + link + '\n')
        # Опрелеляем заголовок
        try:
            title = _soup_.find('div', {'class':'clearfix'}).find('h1').text
            f.write('HEADER: ' + ''.join([c if c not in ['\n','\t'] else '' for c in title]) + '\n')
        except:
            f.write('HEADER: ' + 'No Header' + '\n')
        # Находим данные, если есть
        ps = _soup_.find_all('p')
        data = ''
        try:
            for p in ps:
                data += p.text + '\n'
        except:
            pass
        f.write('CONTENT: ')
        f.write(data)
        # находим дату, если есть
        date = ''
        try:
            date = ''.join([c if c not in ['\n','\t'] else '' for c in _soup_.find('div', {'class': 'node-meta__date'}).text])
        except Exception as e:
            date = 'no date '
        f.write('DATE: ' + date + '\n')
        f.write('\n')
        # определяем тэги
        try:
            tags = _soup_.find('div', {'class': 'block-atom-sidebar-taxonomy block block-atom-sidebar clearfix'})
            content = tags.find('div', {'class': 'content'}).find_all('div', class_="title")
            f.write('TAGS: ')
            t = []
            for tag in content:
                te = tag.find('a').text
                sp = tag.find('span').text
                f.write(te + sp + ' ')
                t.append(te + sp + ' ')
            f.write('\n')
        except Exception as e:
            f.write('TAGS: ' + '\n')

        f.write(''.join(['-' for i in range(50)]) + '\n')

        try:
            key_ = link
            data_ = data
            date_ = date
            tags_ = t
            if elasticsearchCrawlerClient.contains(key_):
                pass
            else:
                elasticsearchCrawlerClient.put(key_, data_, date_, tags_)
        except:
            pass
