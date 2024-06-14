import os
import re
import json
import time
import requests
import wikipedia
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


# /Users/lianamardanova/Downloads/chromedriver-mac-arm64/chromedriver
service = Service(executable_path='/Users/lianamardanova/Downloads/chromedriver-mac-arm64/chromedriver')
# service = Service(executable_path='chromedriver-win64\chromedriver-win64\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


def url_search(file_path):
    search_url = 'https://yandex.ru/images/search'
    files = {'upfile': ('blob', open(file_path, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(search_url, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = search_url + '?' + query_string

    return img_search_url


def get_names(file_path):
    img_search_url = url_search(file_path)
    driver.get(img_search_url)

    search_srt = 'CbirTags'

    driver.page_source[driver.page_source.find(search_srt):]

    data_state = []

    for ind in [m.start() for m in re.finditer(search_srt, driver.page_source)]:
        if 'data-state' not in driver.page_source[ind - 100: ind + 100]:
            continue

        data_state = driver.page_source[ind - 100: ind + 100000].split('data-state=')[1].split('[', 1)[1].split('},')
        for i in range(min(3, len(data_state))):
            data_state[i] = data_state[i].split('&quot;text&quot;:&quot;')[1].split('&quot')[0]

    return data_state[:3]


def get_wiki_link(painting_name):
    google_url = "https://www.google.com"

    # Open Google
    driver.get(google_url)

    # Find the search box, input the query, and submit it
    search_query = painting_name + " website:wikipedia.org"
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(1)

    # Find all search result elements
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")

    links = []
    # Extract and print the title and URL of each search result
    for i, result in enumerate(search_results):
        title_element = result.find_element(By.CSS_SELECTOR, "h3")
        title = title_element.text
        link_element = result.find_element(By.CSS_SELECTOR, "a")
        link = link_element.get_attribute("href")
        links.append(link)

        if 'ru.wikipedia.org' in link:
            return link

    return links


def get_wiki_title(link):
    driver.get(link)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    title = soup.find(id='firstHeading')

    infobox = soup.find(class_='infobox')  # Locate the infobox container
    if infobox:
        image = infobox.find('img')
        if image:
            image_url = image['src']
            if image_url[:2] == '//':
                image_url = 'https:' + image_url

            # Download the image (optional)
            image_response = requests.get(image_url)
            extension = image_url.split('.')[-1]
            print(extension)
            title = title.text.strip().replace(" ", '_')
            print(title)
            with open(f'static/saved_images/{title}.{extension}', 'wb') as f:
                f.write(image_response.content)

    return title, extension


import torchvision
import torch
from PIL import Image
from numpy import dot
from numpy.linalg import norm
import os
from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights

def get_similarity(img_path):
    model = mobilenet_v3_large(weights=MobileNet_V3_Large_Weights.IMAGENET1K_V2)

    model.eval()

    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    IMG_SIZE = 512
    transforms = torchvision.transforms.Compose([
        torchvision.transforms.Resize((IMG_SIZE, IMG_SIZE),
                                      interpolation=torchvision.transforms.InterpolationMode.BILINEAR),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(mean, std)
    ])

    model.classifier = model.classifier[0]

    def get_emb(img_path):
        img = Image.open(img_path)

        img_normalized = transforms(img).float()
        img_normalized = img_normalized.unsqueeze_(0)

        with torch.no_grad():
            model.eval()
            output = model(img_normalized)
            return output.data.cpu().numpy().tolist()[0]

    emb1 = get_emb(img_path)

    names = get_names(img_path)
    link = get_wiki_link(sorted(names, key=lambda x: len(x))[-1])
    title, extention = get_wiki_title(link)

    second_path = os.path.join('saved_images', f'{title}.{extention}')

    emb2 = get_emb(second_path)

    def cos_sim(a, b):
        return dot(a, b) / (norm(a) * norm(b))

    sim = int(cos_sim(emb1, emb2) * 100)

    if sim < 20:
        return False, 0, title.replace('_', ' '), second_path

    return True, sim, title.replace('_', ' '), second_path

def get_full_info(file_path, num_sentences=4):
    names = get_names(file_path)
    link = get_wiki_link(sorted(names, key=lambda x: len(x))[-1])

    title, extension = get_wiki_title(link)

    title = title.replace('_', ' ')

    wikipedia.set_lang('ru')
    info = wikipedia.summary(title).split('\n\n')[0]

    title = title.replace(' ', '_')

    if len(info) > 500:
        return info[:500] + "...", link, os.path.join('saved_images', f'{title}.{extension}')
    return info, link, os.path.join('saved_images', f'{title}.{extension}')

