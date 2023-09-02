import os
import os.path
from os.path import join, dirname
import shutil
import uuid
import concurrent.futures

from dotenv import load_dotenv
import requests
import argparse

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
API_KEY = os.environ.get("API_NINJAS_KEY")
SAVE_PATH = os.environ.get("SAVE_IMAGES_PATH")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-c', '--count', type=int)
arg_parser.add_argument('-t', '--type', type=str)
arg_parser.add_argument('-ww', '--width', type=int)
arg_parser.add_argument('-hh', '--height', type=int)
args = arg_parser.parse_args()

count = args.count or 1
category = args.type or 'abstract'
width = args.width or 640
height = args.height or 480
api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category) \
          + '&width={}'.format(width) + '&height={}'.format(height)


def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'wb')


def download_image(url):
    response = requests.get(
        url=url,
        headers={'X-Api-Key': API_KEY, 'Accept': 'image/jpg'},
        stream=True
    )

    if not response.ok:
        return print("Error:", response.status_code, response.text)

    with safe_open_w(f'{SAVE_PATH}/{uuid.uuid1()}.jpg') as file:
        shutil.copyfileobj(response.raw, file)


with concurrent.futures.ThreadPoolExecutor() as executor:
    urls = [api_url] * count
    executor.map(download_image, urls)
