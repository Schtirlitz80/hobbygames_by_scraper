"""
Используя данные json файла, формирует новый, добавляя номер к каждому из продуктов, и скачивая картинки
по ссылкам из исходного файла. Новый json и картинки к нему сохраняем в папку products
"""

import json
import urllib.request
import os

final_data = []
with open('hobbygames_products2.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    images_quantity = len(data)

    for num, p in enumerate(data):
        print(f"Processing image {num} of {images_quantity}")
        product_name = p['product_name']
        price = p['price']
        short_description = p['short_description']
        full_description = p['full_description']
        main_picture_url = p['main_picture_url']
        pictures = p['pictures']

        image_filepath = os.path.join("products2", str(num))
        print(image_filepath)
        print(os.path.exists(image_filepath))
        if not os.path.exists(image_filepath):
            os.makedirs(image_filepath)

        image_filenames = []

        try:
            for pic_num, pic_url in enumerate(pictures):
                r = urllib.request.urlopen(pic_url)
                # with open(f"products2/{product_name}/{image_filename}", "wb") as f:
                # filename = f"{image_filepath}/{pic_num}.jpg"
                filename = f"{pic_num}.jpg"
                with open(f'{image_filepath}/ {filename}', "wb") as f:
                    f.write(r.read())
                image_filenames.append(filename)

        except Exception as _ex:
            print(_ex)
            continue

        item_data = {
            'num': num,
            'product_name': product_name,
            'price': price,
            'short_description': short_description,
            'full_description': full_description,
            'image_filenames': image_filenames
        }

        final_data.append(item_data)

with open('products2/products.json', 'w', encoding='utf-8') as file:
    json.dump(final_data, file, indent=4, ensure_ascii=False)
