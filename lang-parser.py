import requests
import os.path
from pprint import pprint
import json

import pandas

from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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


def get_phrases(url, lang):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        phrase = {}
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        theme_names = soup.find_all('h3', class_='text_lineheight')
        theme_names = [name.text for name in theme_names]
        theme_name = theme_names[1]
        # theme_name = ', '.join(theme_names)
        phrases_1 = soup.find_all('td', class_='nativee_txtt mb-mob-0')
        phrases_1 = [phrase.text for phrase in phrases_1]
        phrases_2 = soup.find_all('span', class_='hide-item phrase-display hide-text-btn text-blue op4')
        phrases_2 = [phrase.text for phrase in phrases_2]
        phrases_3 = soup.find_all('span', class_='option3 hide-item phrase-display transliteration-text hide_all_each')
        phrases_3 = [phrase.text for phrase in phrases_3]
        keys = ['rus', f'{lang}_1', f'{lang}_2']
        zipped = zip(phrases_1, phrases_2, phrases_3)
        phrases_dicts = [dict(zip(keys, values)) for values in zipped]
        phrases_dicts.insert(0, theme_name)
        return phrases_dicts
    else:
        print(f'========== PRODUCTS - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False


def save_json(response, file='loft_data.json'):
    with open(f'{file}', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False)


def main():
    langs = ['ko', 'ja']

    for lang in langs:
        search_url = f'https://www.50languages.com/ru/learn/phrasebook/{lang}'
        out_data_name = f'rus_{lang}_themes'
        count = 1
        theme_urls = get_themes(search_url)
        themes = []
        if theme_urls:
            for url in theme_urls:
                print(f'{count}. {url}')
                phrases = get_phrases(url, lang)
                for phrase in phrases:
                    print(phrase)
                    themes.append(phrase)
                count += 1
                # break
            
        save_json(themes, file=f'{out_data_name}.json')
        pandas.read_json(f"{out_data_name}.json").to_excel(f"{out_data_name}.xlsx")


if __name__ == '__main__':
    main()






