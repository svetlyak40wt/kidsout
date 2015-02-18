#!/usr/bin/env python3

import re
import requests
import os
from config import COOKIES
from itertools import islice


ANKETS_DIR = 'ankets'
BASE_URL = 'https://kidsout.ru'


def make_request(url):
    return requests.get(BASE_URL + url,
                        headers={'Accept': 'application/json',
                                 'Cookie': COOKIES})

def get_sitters():
    def recur(page):
        response = make_request('/?page={0}'.format(page))
        data = response.json()
        for sitter in data['sitters']:
            yield sitter

        if data['meta']['total_page'] > page:
            yield from recur(page + 1)
    return recur(page=1)


_content_type = ('<meta http-equiv="Content-Type"'
                       'content="text/html; charset=UTF-8" />')

def download_anket(sitter):
    response = make_request(sitter['url'])
    filename = os.path.join(ANKETS_DIR, sitter['token'] + '.html')
    with open(filename, 'w') as f:
        content = response.text
        content = content.replace(
            '</title>',
            '</title>' + \
            _content_type)
        content = re.sub(
            r'<p data-ko-collapse-text="400" text="&#39;(.*?)&#39;">',
            r'<p>\1', content)
        content = re.sub(
            r'src="/',
            r'src="' + BASE_URL + '/',
            content)
        content = re.sub(
            r'href="/',
            r'href="' + BASE_URL + '/',
            content)
        f.write(content)


def download_ankets():
    if not os.path.exists(ANKETS_DIR):
        os.makedirs(ANKETS_DIR)

    sitters = get_sitters()
    for sitter in islice(sitters, 0, 1):
        download_anket(sitter)


print('DOWNLOADING...')
download_ankets()
print('DONE')
