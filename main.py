import requests
from bs4 import BeautifulSoup
import time

BASE_URL = 'https://pastebin.com/'

def get_list_page():
    url = BASE_URL + 'archive'
    return requests.get(url).text

def get_pastes():
    page = get_list_page()
    soup = BeautifulSoup(page, 'lxml')
    return [
        {'name': a.text,
         'url': BASE_URL + a['href'],
         'id': a['href'].strip('/')}
        for a in soup.select('table.maintable tr a ')]

def get_paste_text(id):
    url = f'{BASE_URL}raw/{id}'
    return requests.get(url).text

def contains_interesting_info(text):
    buzz_word = ['api_key', 'password', 'login', 'email', 'username', '0x']
    for word in buzz_word:
        if word in text:
            return True

def main():
    # print(type(get_pastes()))
    # print(get_paste_text(get_pastes()))
    seen_paste_ids = set()
    while True:
        pastes = get_pastes()
        for i, paste in enumerate(pastes):
            print(i)
            print(paste['id'])
            if paste['id'] not in seen_paste_ids:
                text = get_paste_text(paste['id'])
                if contains_interesting_info(text):
                    print(text)
                seen_paste_ids.add(paste['id'])
        time.sleep(60)

if __name__ == '__main__':
    main()