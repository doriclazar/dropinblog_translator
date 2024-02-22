import requests
import html
from urllib.parse import quote, unquote

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

    def translate_dashed(self, string, language_abbreviation):
        separated_string = str(string).replace('-', '')
        parsed_string =  quote(separated_string, safe='/', encoding=None, errors=None)
        data = (
            f'async=translate,sl:auto,tl:{language_abbreviation},st:{parsed_string},id:0000000000030,qc:true,ac:false,_id:tw-async-translate,_pms:s,_fmt:pc')
        response = requests.post('https://www.google.com/async/translate', headers=self.headers, data=data)
        translation = BeautifulSoup(response.content, 'lxml')
        translated_string = translation.find('span', {'id': 'tw-answ-target-text'}).text
        return translated_string.replace(' ', '-')

    def translate_string(self, string, language_abbreviation):
        parsed_string = quote(string, safe='/', encoding=None, errors=None)
        data = (
            f'async=translate,sl:auto,tl:{language_abbreviation},st:{parsed_string},id:0000000000030,qc:true,ac:false,_id:tw-async-translate,_pms:s,_fmt:pc')
        response = requests.post('https://www.google.com/async/translate', headers=self.headers, data=data)
        translation = BeautifulSoup(response.content, 'lxml')
        translated_string = translation.find('span', {'id': 'tw-answ-target-text'}).text
        return translated_string

    def _write_to_file(self, post_code):
        with open('finito_fr.html', 'w', encoding='utf-8') as translation_file:
            translation_file.write(post_code.prettify(formatter=None))
            # translation_file.write(str(post_code))
            # translation_file.write(html.unescape(str(post_code.encode('utf-8'))))

    def translate_content(self, post_code, language_abbreviation):
        for element in post_code.find_all(['h3', 'h4', 'li', 'h1', 'h2', 'p']):
            # if element.text.count('>') > 3:
            if '<img' in str(element):
                continue
            string_slice = quote(element.text, safe='/', encoding=None, errors=None)
            data = (f'async=translate,sl:auto,tl:{language_abbreviation},st:{string_slice},id:0000000000030,qc:true,ac:false,_id:tw-async-translate,_pms:s,_fmt:pc')
            response = requests.post('https://www.google.com/async/translate', headers=self.headers, data=data)
            # response.encoding = 'UTF-8'
            translation = BeautifulSoup(response.text, 'lxml')
            translation_string = translation.find('span', {'id': 'tw-answ-target-text'}).text
            # if '   ' in translation_string:
                # translation_string = translation.find('span', {'id': 'tw-answ-romanization'}).text

            # translation_string = translation_string.encode('ascii', 'ignore').decode('utf-8')
            # try:
                # print(translation_string)
            # except UnicodeEncodeError:
                # translation_string = translation_string.encode('ascii', 'ignore').decode('utf-8')
                # print(translation_string)


            # new_element = str(tag_open + translation_string + tag_close)
            # element.replace_with(new_element)
            element.string = translation_string
            # print(element)

        # self._write_to_file(post_code)
        return post_code