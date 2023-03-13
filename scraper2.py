from bs4 import BeautifulSoup
import requests
from pprint import pprint
import os
import json

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

# Ниже закомментили блок кода для получения списка ссылок, по которым будем получать информацию о товарах
# Поскольку эту операцию нужно выполнить только один раз, то после успешного выполнения её и комментим...
# product_urls = []
# for page in range(1, 96):
#     print(f'Страница {page}/96')
#     result = requests.get(f'https://hobbygames.by/nastolnie-igri?page={page}&parameter_type=0', headers=headers)
#     content = result.text
#
#     soup = BeautifulSoup(content, 'lxml')
#     print(type(soup))
#
#     product_list = soup.find_all('div', class_='product-item__content')
#
#     for i, product in enumerate(product_list):
#         print(f'Страница {page}/96 продукт {i}')
#         url = product.find('div', class_='image').find('a').attrs['href']
#         product_urls.append(url)
#
# pprint(product_urls)
# print(len(product_urls))
# if not os.path.exists('hobbygames_urls'):
#     os.mkdir('hobbygames_urls')
# with open('hobbygames_urls/product_urls.txt', 'w', encoding='utf-8') as file:
#     for product in product_urls:
#         file.writelines(f'{product}\n')

product_urls = []
with open('hobbygames_urls/product_urls.txt', encoding='utf-8') as file:
    while True:
        line = file.readline().strip()
        if not line:
            break
        product_urls.append(line)

# print(product_urls)
product_data_list = []
quantity = len(product_urls)

for i, url in enumerate(product_urls[:100]):
    print(f'Обрабатываю {i} товар из {quantity}')

    try:
        result = requests.get(url=url, headers=headers)

        content = result.text
        soup = BeautifulSoup(content, 'lxml')

        product_name = soup.find('div', class_='product-info__main').find('h1').text.strip()
        price = soup.find('div', class_='price-item').text.strip()
        short_description = soup.find('div', class_='row product-box').find('div', class_='desc').text.strip()
        full_description = soup.find('div', class_='desc-text').text.strip()
        main_picture_url = soup.find('picture').find('img').get('data-src')

        pictures = []
        pcs = soup.find('ul', id='lightSlider').find_all('a', class_='lightGallery')
        print(type(pcs))
        for pic in pcs:
            pictures.append(pic.get('href'))


    except Exception as _ex:
        print(_ex)
        continue

    item_data = {
        'product_name': product_name,
        'price': price,
        'short_description': short_description,
        'full_description': full_description,
        'main_picture_url': main_picture_url,
        'pictures': pictures,
    }

    print(item_data)

    # pprint(item_data)
    product_data_list.append(item_data)

with open('hobbygames_products2.json', 'w', encoding='utf-8') as file:
    json.dump(product_data_list, file, indent=4, ensure_ascii=False)
