import requests
from bs4 import BeautifulSoup as bs
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}

base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1001&clusters=true&enable_snippets=true&text=python&page=0'

def hh_parse(base_url, headers):
    jobs = []
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', class_='vacancy-serp-item' )
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text 
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            response = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            require = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            all_inf = response + ' ' + require
            jobs.append({'title': title,
                         'company': company,
                         'Content': all_inf,
                         'href': href
                         })

        print(len(jobs))
    else:
        print("ERROR")

hh_parse(base_url, headers)

    #print(request)


