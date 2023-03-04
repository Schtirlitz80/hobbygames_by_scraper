"""
Используя данные json файла, формирует новый, добавляя номер к каждому из продуктов, и скачивая картинки
по ссылкам из исходного файла. Новый json и картинки к нему сохраняем в папку products
"""

import json
import urllib.request

final_data = []
with open('hobbygames_products.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    images_quantity = len(data)

    for num, p in enumerate(data):
        print(f"Processing image {num} of {images_quantity}")
        product_name = p['product_name']
        price = p['price']
        short_description = p['short_description']
        full_description = p['full_description']
        main_picture_url = p['main_picture_url']

        image_filename = f"{num}.jpg"

        try:
            r = urllib.request.urlopen(main_picture_url)
            with open(f"products/{image_filename}", "wb") as f:
                f.write(r.read())
        except Exception as _ex:
            print(_ex)
            continue

        item_data = {
            'num': num,
            'product_name': product_name,
            'price': price,
            'short_description': short_description,
            'full_description': full_description,
            'image_filename': image_filename
        }

        final_data.append(item_data)

with open('products/products.json', 'w', encoding='utf-8') as file:
    json.dump(final_data, file, indent=4, ensure_ascii=False)
