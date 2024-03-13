import requests
import os
import os.path

from bs4 import BeautifulSoup

proxies = {
#    'http': 'socks5://ZGTxtv:gnttyS@194.67.214.57:9658',
#    'https': 'socks5://ZGTxtv:gnttyS@194.67.214.57:9658',
   'http': 'socks5://wGJX8p:unz2MG@88.218.72.74:9060',
   'https': 'socks5://wGJX8p:unz2MG@88.218.72.74:9060',
}

# from database.orm import create_download, get_manual_titles_from_donor


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
base_url = 'https://www.emaselectric.com'
base_product_url = 'https://www.emaselectric.com/products'
test_url = 'https://www.emaselectric.com/products/b--control-boxes'
images_path = 'images'


def get_products(url):
    response = requests.post(url=url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'windows-1251'
        soup = BeautifulSoup(response.text, 'lxml')
        uls = soup.find_all('ul', class_='nav panel-group')
        products = uls[1].find_all('a')
        products = [base_url + product['href'] for product in products]
        return products
    else:
        print(f'========== PRODUCTS - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False
    

def get_series(url):
    series = []
    response = requests.post(url=url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'windows-1251'
        soup = BeautifulSoup(response.text, 'lxml')
        divs = soup.find_all('div', class_='col-sm-6 col-md-3 top20 product')
        series = [base_url + div.find('a')['href'] for div in divs]
        return series
    else:
        print(f'========== SERIES - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False
    

def download_file(url):
    filename = url.split('/')[-1]
    response = requests.get(url=url, headers=headers)
    path = f'{images_path}/{filename}'
    if response.status_code == 200:
        with open(path, mode="wb") as file:
                file.write(response.content)
        return filename
    else:
        print(f'========== FILE - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False


def get_images(url):
    images_all = []
    response = requests.post(url=url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'windows-1251'
        soup = BeautifulSoup(response.text, 'lxml')
        div = soup.find('div', class_='col-sm-8 col-md-9 shop')
        images = div.find_all('div', class_='thumbnail')
        for image in images:
            try:
                img = image.find('img')['src']
                img = img.replace('?format=webp&w=202&h=135&scale=both', '')
                if img.find('no-image.jpg') < 0:
                    img = img.replace('thumbs/thumbs/', '')
                    images_all.append(base_url + img)
            except:
                # images_all.append('NO IMAGE')
                pass
        return images_all
    else:
        print(f'========== IMAGES - RESPONSE ERROR! RESPONSE STATUS CODE: {response.status_code}')
        return False


def main():
    count = 1
    products = get_products(base_product_url)
    for product in products:
        if products:
            series = get_series(product)
            if series:
                for serie in series:
                    images = get_images(serie)
                    if images:
                        for image in images:
                            download_file(image)
                            print(f'{count}. {image}')
                            count += 1
                        # return

if __name__ == '__main__':
    main()






