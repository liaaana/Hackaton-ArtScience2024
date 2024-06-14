import base64
import requests


def search_artwork_details(image_path, api_key, cx):
    """
    Находит название и автора картины по изображению.

    :param image_path: Путь к изображению картины.
    :param api_key: API ключ для Google Custom Search API.
    :param cx: Идентификатор движка поиска (cx) для Custom Search Engine.
    :return: Название картины и автор.
    """
    search_url = "https://www.googleapis.com/customsearch/v1"

    # Загрузите изображение и закодируйте его в base64
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    params = {
        'q': 'painting',
        'searchType': 'image',
        'key': api_key,
        'cx': cx,
        'imgSize': 'large',
        'num': 1,
        'fileType': 'jpg',
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.get(search_url, params=params, headers=headers)

    if response.status_code == 200:
        search_results = response.json()
        print(search_results)
        if 'items' in search_results and search_results['items']:
            item = search_results['items'][0]
            title = item.get('title')
            link = item.get('link')
            return title, link
        else:
            return None, None
    else:
        response.raise_for_status()


# Пример использования:
api_key = 'AIzaSyBGkJ5ELVv0rgX3MQ2SrdZxc1RQzdT_-Pc'
cx = '0519131675d6a4c7f'
image_path = './static/uploads/d9aaa26ba2e1288d.jpg'
title, author = search_artwork_details(image_path, api_key, cx)

if title and author:
    print(f'Название картины: {title}')
    print(f'Автор картины: {author}')
else:
    print('Информация о картине не найдена.')
