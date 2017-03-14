# speechpro_wrapper

Эта обёртка позволяет использовать инструмент для перевода текста в голос Центра Речевых Технологий http://www.speechpro.ru/ бесплатно.

Требования:

GNU/Linux or Windows

Python3

pip install -r requirements.txt

python3 center_speech_to_voice.py 'Тут ваша строка для перевод текста в речь на русском языке'

#IPython Console

Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:54:25) [MSC v.1900 64 bit (AMD64)] on win32
In[2]: from center_speech_to_voice import SessionSpeech
In[4]: SPEECH_PRO_WAV = 'http://www.speechpro.ru/voice-fabric/text-to-voice/'
SPEECHPRO_URL = 'http://www.speechpro.ru/'
In[3]: c = SessionSpeech(SPEECHPRO_URL, SPEECH_PRO_WAV)
In[6]: text = 'Например, вот такой текст, всё равно что тут будет:) и даже если 2323445 миллионов...'
In[7]: c.text_to_speech(text)


This wrapper allows you to use the API Center for Speech Technology http://www.speechpro.ru/ for free without SMS and registration ...

Works only with the Russian language.

Requirements:

Python3

pip install -r requirements.txt

GNU/Linux or Windows

