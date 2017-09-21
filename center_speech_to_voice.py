#!/usr/bin/env python3
import sys
import wave
import shutil

import pyaudio
from requests import Session, post, get

SPEECH_PRO_WAV = 'http://www.speechpro.ru/voice-fabric/text-to-voice'
SPEECHPRO_URL = 'http://www.speechpro.ru/'


class SessionSpeech:
    """download wav from speechpro"""

    def __init__(self, url, url_download):
        self.url = url
        self.download_url = url_download
        self.ses = Session()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': 1,
            'Host': 'www.speechpro.ru',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36',
        }
        res = self.ses.get(url)
        self.csrftoken = res.headers['Set-Cookie'].split(';')[0].split('=')[1]
        self.cookie = self.ses.cookies.get_dict()['sessionid']

    def text_to_speech(self, text_to_voice, listen=False, path='.'):
        cookies = {
            'sessionid': self.cookie,
            'csrftoken': self.csrftoken,
        }

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://www.speechpro.ru',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36',
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
             text_to_voice),
            ('csrfmiddlewaretoken', self.csrftoken),
        ]

        res = post(self.download_url, headers=headers, cookies=cookies, data=data)
        wav_url = res.json()['response']
        wav_url_file = headers['Origin'] + '/' + wav_url
        chunk = 1024
        r = get(wav_url_file, stream=True)
        if listen:
            wf = wave.open(r.raw, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(
                    format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
            data = wf.readframes(chunk)

            while data != '':
                stream.write(data)
                data = wf.readframes(chunk)

            stream.close()
            p.terminate()
        else:
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)


if __name__ == "__main__":
    c = SessionSpeech(SPEECHPRO_URL, SPEECH_PRO_WAV)
    try:
        text = sys.argv[1]
    except IndexError:
        text = 'Например, вот такой текст, всё равно что тут будет:) и даже если 2323445 миллионов...'
    c.text_to_speech(text, listen=False, path='file.wav') #Path путь для сохранения файла.
