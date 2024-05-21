import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse


def shorten_link(token, link):
     url = "https://api-ssl.bitly.com/v4/shorten"
     body = {
         "long_url": link,
     }
     headers = {
        'Authorization': f'Bearer {token}'
     }
     response = requests.post(url, json=body,  headers=headers)
     response.raise_for_status()
     return response.json()['link']            


def count_clicks(link, token):
    bitlink = urlparse(link)
    bitlink = f"{bitlink.netloc}{bitlink.path}"
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']   


def is_bitlink(link, token):
    bitlink = urlparse(link)
    bitlink = f"{bitlink.netloc}{bitlink.path}"
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Создаёт битлинки или выводит количество кликов по ним')
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()

    bitly_token = os.getenv('BITLY_TOKEN')
    try:
        if is_bitlink(args.link, bitly_token):
            print("Кол-во кликов: ", count_clicks(args.link, bitly_token)) 
        else:
            bitlink = shorten_link(bitly_token, args.link)
            print('Битлинк: ', bitlink)
    except requests.exceptions.HTTPError:
        print('В вашей ссылке присутствует ошибка!')


if __name__ == '__main__':
    main()