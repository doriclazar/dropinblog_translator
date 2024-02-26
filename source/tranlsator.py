import logging
import requests
from urllib.parse import quote, unquote
from unidecode import unidecode
from bs4 import BeautifulSoup

class Translator:
    def __init__(self):
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'origin': 'https://www.google.com',
            'preferanonymous': '1',
            'referer': 'https://www.google.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"121.0.2277.128"',
            'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.128", "Chromium";v="121.0.6167.184"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'x-dos-behavior': 'Embed',
        }

    def translate_dashed(self, string, language_abbreviation, romanize=False, uni=False):
        separated_string = str(string).replace('-', ' ')
        parsed_string =  quote(separated_string, safe='/', encoding=None, errors=None)
        data = (
            f'async=translate,sl:auto,tl:{language_abbreviation},st:{parsed_string},id:0000000000030,qc:true,ac:false,_id:tw-async-translate,_pms:s,_fmt:pc')
        response = requests.post('https://www.google.com/async/translate', headers=self.headers, data=data)
        translation = BeautifulSoup(response.content, 'lxml')
        translated_string = translation.find('span', {'id': 'tw-answ-target-text'}).text
        if romanize:
            try:
                romanization_string = translation.find('span', {'id': 'tw-answ-romanization'}).text
                if romanization_string.replace(' ', ''):
                    translated_string = romanization_string
            except Exception as ex:
                logging.error(ex)
            if uni:
                translated_string = unidecode(translated_string)

        return translated_string.replace(' ', '-').replace("'", '').replace('@', '')

    def translate_string(self, string, language_abbreviation, romanize=False):
        parsed_string = quote(string, safe='/', encoding=None, errors=None)
        data = (
            f'async=translate,sl:auto,tl:{language_abbreviation},st:{parsed_string},id:0000000000030,qc:true,ac:false,_id:tw-async-translate,_pms:s,_fmt:pc')
        response = requests.post('https://www.google.com/async/translate', headers=self.headers, data=data)
        translation = BeautifulSoup(response.content, 'lxml')
        translated_string = translation.find('span', {'id': 'tw-answ-target-text'}).text
        if romanize:
            try:
                romanization_string = translation.find('span', {'id': 'tw-answ-romanization'}).text
                if romanization_string.replace(' ', ''):
                    translated_string = romanization_string
            except Exception as ex:
                logging.error(ex)
        return translated_string.replace("'", '').replace('@', '')

    def _write_to_file(self, post_code):
        with open('finito_fr.html', 'w', encoding='utf-8') as translation_file:
            translation_file.write(post_code.prettify(formatter=None))

    def translate_content(self, post_code, language_abbreviation):
        for element in post_code.find_all(['h1', 'h2', 'h3', 'h4', 'li', 'p', 'a', 'link']):
            if '<img' in str(element):
                continue
            string_slice = quote(element.text, safe='/', encoding=None, errors=None)
            data = (f'async=translate,sl:auto,tl:{language_abbreviation},st:{string_slice},id:0000000000030,qc:true,ac:false,_id:tw-async-translate,_pms:s,_fmt:pc')
            response = requests.post('https://www.google.com/async/translate', headers=self.headers, data=data)
            translation = BeautifulSoup(response.text, 'lxml')
            translation_string = translation.find('span', {'id': 'tw-answ-target-text'}).text
            element.string = translation_string

        for element in post_code.find_all('img'):
            cur_location, cur_name = element.attrs['data-lazy-load'].rsplit('/', 1)
            extension = '.' + cur_name.split('.')[-1].lower()
            translated_name = self.translate_dashed(cur_name.replace(extension, ''), language_abbreviation, romanize=True, uni=True).replace('|', '')

            img_data = requests.get(element.attrs['data-lazy-load']).content
            translated_path = 'data/' + translated_name + extension
            with open(translated_path, 'wb') as handler:
                handler.write(img_data)

            element.attrs['src'] = cur_location + '/' + translated_name + extension

        post_code.find('html').unwrap()
        post_code.find('body').unwrap()

        return post_code