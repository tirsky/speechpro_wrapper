import json
import logging
import sys
import zipfile

import io
import os
from copy import deepcopy
from requests import Request, Session, get, post

url_download = 'http://www.speechpro.ru/voice-fabric/text-to-voice/'
url = 'http://www.speechpro.ru/'


class SessionSpeech:
    """download wav from speechpro"""

    def __init__(self, url, url_download):
        self.url = url
        self.download_url = url_download
        self.ses = Session()
        self.headers = {}
        self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self.headers['Accept-Encoding'] = 'gzip, deflate, sdch'
        self.headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
        self.headers['Cache-Control'] = 'no-cache'
        self.headers['Connection'] = 'keep-alive'
        self.headers['DNT'] = 1
        self.headers['Host'] = 'www.speechpro.ru'
        self.headers['Pragma'] = 'no-cache'
        self.headers['Upgrade-Insecure-Requests'] = 1
        self.headers[
            'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36'

        res = self.ses.get(url)
        self.csrftoken = res.headers['Set-Cookie'].split(';')[0].split('=')[1]
        self.cookie = self.ses.cookies.get_dict()['sessionid']

    def download(self):
        cookies = {
            'sessionid': self.cookie,
            'csrftoken': self.csrftoken,
        }

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://www.speechpro.ru',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'http://www.speechpro.ru',
            'DNT': '1',
        }

        data = [
            ('text',
             'Вот это даа! Работает, собака!'),
            ('csrfmiddlewaretoken', self.csrftoken),
        ]

        res = post('http://www.speechpro.ru/voice-fabric/text-to-voice', headers=headers, cookies=cookies, data=data)
        wav_url = res.json()['response']
        wav = headers['Origin'] + '/' + wav_url
        os.system('mplayer ' + wav)


if __name__ == "__main__":
    c = SessionSpeech(url, url_download)
    c.download()
