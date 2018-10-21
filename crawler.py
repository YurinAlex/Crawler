import requests
import os
# from lxml import html
from bs4 import BeautifulSoup

header = {'User-Agent':
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
url_majors = 'http://www.atomic-energy.ru/'
links = ('why-nuclear', '2.0')

req = requests.get(url_majors, headers = header)
soup = BeautifulSoup(req.text)
li = soup.find('nav').find('ul').find_all('li')

mass = []
for l in li:
    l.find('a', href = True)
    href = l.find('a', href = True)['href']
    if 'http' in href or href == '/':
        continue
    loc_req = requests.get(url_majors+href, headers = header)

    soup = BeautifulSoup(loc_req.text)
    dir = os.path.abspath(os.curdir)
    with open(dir+'/'+href.split('/')[-1]+'.txt','w') as f:
        title = soup.find('div', {'class':'clearfix'}).find('h1').text
        f.write(title + '\n')
        ps = soup.find_all('p')
        for p in ps:
            f.write(p.text + '\n')

    for x in soup.find_all('a'):
        if ':' in x['href']:
            continue
        elif x['href'] in mass:
            continue
        mass.append(x['href'])
        try:
            if not os.path.exists(dir+'/'+'files'+'/'):
                os.makedirs(dir+'/'+'files'+'/')
            name = ''.join(c if c not in ['/','?','='] else '' for c in x['href'][1:])
            with open(dir+'/'+'files'+'/'+name+'.txt', 'w') as f1:
                ll_rec = requests.get(url_majors+x['href'], headers = header)
                loc_soup = BeautifulSoup(ll_rec.text)
                for te in loc_soup.find_all('p'):
                    f1.write(te.text + '\n')
                # Теги
                tags = loc_soup.find('div', {'class': 'block-atom-sidebar-taxonomy block block-atom-sidebar clearfix'})
                content = tags.find('div', {'class': 'content'})
                f1.write(content.text + '\n')
        except Exception as e:
            pass
