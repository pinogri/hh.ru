# 1. парсер однопоточный
# 2. замер времени

import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}

def get_html(url):
    r = requests.get(url)  # Response
    return r.text  # Возвращает HTML код страницы (url)


def get_all_html(html):
    soup = BeautifulSoup(html, "lxml")
    tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')
    links = []
    for td in tds:
        a = td.find('a').get('href')  # string
        link = "https://coinmarketcap.com" + a
        links.append(link)
    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = text_before_word(soup.find('title').text, 'price')
    except:
        name = ''
    try:
        price = text_before_word(soup.find('div',
                                           class_='col-xs-6 col-sm-8 col-md-4 text-left').text, 'USD')
    except:
        price = ''
    data = {'name': name,
            'price': price}
    return data



def write_csv(data):
    with open('marketcap.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow( (data['name'],
                          data['price']) )
        print(data['name'], 'parsed')




def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'
    all_links = [get_all_html(get_html(url))]
    for index, url in enumerate(all_links):
        html = get_html(url)
        data = get_page_data(html)
        write_csv(data)
    end = datetime.now()
    total = end - start
    print (total)

if __name__ == "__main__":
    main()
