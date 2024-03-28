import requests
import os.path
from pprint import pprint
import json

import pandas

from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
search_url = 'https://www.loft2rent.ru/loft/?city=65322&text=&price_start=&price_end=&people_start=&people_end=&area_start=&area_end=&party_date='
base_url = 'https://www.loft2rent.ru'

def get_loft_urls(url):
    response = requests.post(url=url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'windows-1251'
        soup = BeautifulSoup(response.text, 'lxml')
        loft_divs = soup.find_all('div', class_='card loft')
        card_divs = [div.find('div', class_='card-body') for div in loft_divs]
        card_urls = [base_url + card.find('a', class_='card-title')['href'] for card in card_divs]
        return card_urls
    else:
        print(f'========== PRODUCTS - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False


def get_loft(url):
    response = requests.post(url=url, headers=headers)
    if response.status_code == 200:
        loft = {}
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        loft['loft_name'] = soup.find('h1', class_='h1loft').text
        loft['loft_street'] = soup.find('span', {'itemprop': 'streetAddress'}).text
        try:
            loft['loft_email'] = soup.find('a', {'itemprop': 'email'}).text
        except:
            loft['loft_email'] = 'NO EMAIL'
        loft['loft_phone'] = soup.find('a', {'itemprop': 'telephone'}).text
        
        return loft
    else:
        print(f'========== PRODUCTS - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False


def save_json(response, file='loft_data.json'):
    with open(f'{file}', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False)


def main():
    count = 1
    lofts = []
    loft_urls = get_loft_urls(search_url)
    for loft_url in loft_urls:
        print(f'{count}. {loft_url}')
        count += 1
        loft = get_loft(loft_url)
        pprint(loft)
        lofts.append(loft)
        
    save_json(lofts)
    pandas.read_json("loft_data.json").to_excel("loft_data.xlsx")


if __name__ == '__main__':
    main()






