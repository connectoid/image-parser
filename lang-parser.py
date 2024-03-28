import requests
import os.path
from pprint import pprint
import json

import pandas

from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
search_url = 'https://www.50languages.com/ru/learn/phrasebook/ko'
base_url = 'https://www.50languages.com'

def get_themes(url):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'windows-1251'
        soup = BeautifulSoup(response.text, 'lxml')
        themes_links = soup.find_all('div', class_='li-lessons')
        themes_links = [link.find('a')['href'] for link in themes_links]
        return themes_links
    else:
        print(f'========== PRODUCTS - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False


def get_phrases(url):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        phrase = {}
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        phrases_1 = soup.find_all('td', class_='nativee_txtt mb-mob-0')
        phrases_1 = [phrase.text for phrase in phrases_1]
        phrases_2 = soup.find_all('span', class_='hide-item phrase-display hide-text-btn text-blue op4')
        phrases_2 = [phrase.text for phrase in phrases_2]
        phrases_3 = soup.find_all('span', class_='option3 hide-item phrase-display transliteration-text hide_all_each')
        phrases_3 = [phrase.text for phrase in phrases_3]
        keys = ['rus', 'lang_1', 'lang_2']
        zipped = zip(phrases_1, phrases_2, phrases_3)
        phrases_dicts = [dict(zip(keys, values)) for values in zipped]
        return phrases_dicts
    else:
        print(f'========== PRODUCTS - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False


def save_json(response, file='loft_data.json'):
    with open(f'{file}', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False)


def main():
    count = 1
    theme_urls = get_themes(search_url)
    rus_korea_themes = []
    if theme_urls:
        for url in theme_urls:
            print(f'{count}. {url}')
            phrases = get_phrases(url)
            for phrase in phrases:
                print(phrase)
                rus_korea_themes.append(phrase)
            count += 1
            # break
        
    save_json(rus_korea_themes, file='rus_korea_themes.json')
    pandas.read_json("rus_korea_themes.json").to_excel("rus_korea_themes.xlsx")


if __name__ == '__main__':
    main()






