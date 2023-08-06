import os
import os.path
from os.path import join, dirname
import shutil
import uuid

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

count = args.count if args.count else 1
category = args.type if args.type else 'abstract'
width = args.width if args.width else 640
height = args.height if args.height else 480
api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category) \
          + '&width={}'.format(width) + '&height={}'.format(height)
i = 0


def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'wb')


while i < count:
    response = requests.get(
        url=api_url,
        headers={'X-Api-Key': API_KEY, 'Accept': 'image/jpg'},
        stream=True
    )

    if response.status_code == requests.codes.ok:
        with safe_open_w(f'{SAVE_PATH}/{uuid.uuid1()}.jpg') as file:
            shutil.copyfileobj(response.raw, file)
    else:
        print("Error:", response.status_code, response.text)
    i += 1
