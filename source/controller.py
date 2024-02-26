import os.path
import logging
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tranlsator import Translator
from scraper import Scraper


class Controller:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.language_abbreviations = {
            "sq": "Albanian",
            "am": "Amharic",
            "ar": "Arabic",
            "hy": "Armenian",
            "as": "Assamese",
            "ay": "Aymara",
            "az": "Azerbaijani",
            "bm": "Bambara",
            "eu": "Basque",
            "be": "Belarusian",
            "bn": "Bengali",
            "bho": "Bhojpuri",
            "bs": "Bosnian",
            "bg": "Bulgarian",
            "ca": "Catalan",
            "ceb": "Cebuano",
            "zh-CN": "Chinese (Simplified)",
            "zh-TW (BCP-47)": "Chinese (Traditional)",
            "co": "Corsican",
            "hr": "Croatian",
            "cs": "Czech",
            "da": "Danish",
            "dv": "Dhivehi",
            "doi": "Dogri",
            "nl": "Dutch",
            "eo": "Esperanto",
            "et": "Estonian",
            "ee": "Ewe",
            "fil": "Filipino (Tagalog)",
            "fi": "Finnish",
            "fr": "French",
            "fy": "Frisian",
            "gl": "Galician",
            "ka": "Georgian",
            "de": "German",
            "el": "Greek",
            "gn": "Guarani",
            "gu": "Gujarati",
            "ht": "Haitian Creole",
            "ha": "Hausa",
            "haw": "Hawaiian",
            "iw": "Hebrew",
            "hi": "Hindi",
            "hmn": "Hmong",
            "hu": "Hungarian",
            "is": "Icelandic",
            "ig": "Igbo",
            "ilo": "Ilocano",
            "id": "Indonesian",
            "ga": "Irish",
            "it": "Italian",
            "ja": "Japanese",
            "jv": "Javanese",
            "kn": "Kannada",
            "kk": "Kazakh",
            "km": "Khmer",
            "rw": "Kinyarwanda",
            "gom": "Konkani",
            "ko": "Korean",
            "kri": "Krio",
            "ku": "Kurdish",
            "ckb": "Kurdish (Sorani)",
            "ky": "Kyrgyz",
            "lo": "Lao",
            "la": "Latin",
            "lv": "Latvian",
            "ln": "Lingala",
            "lt": "Lithuanian",
            "lg": "Luganda",
            "lb": "Luxembourgish",
            "mk": "Macedonian",
            "mai": "Maithili",
            "mg": "Malagasy",
            "ms": "Malay",
            "ml": "Malayalam",
            "mt": "Maltese",
            "mi": "Maori",
            "mr": "Marathi",
            "mni-Mtei": "Meiteilon (Manipuri)",
            "lus": "Mizo",
            "mn": "Mongolian",
            "my": "Myanmar (Burmese)",
            "ne": "Nepali",
            "no": "Norwegian",
            "ny": "Nyanja (Chichewa)",
            "or": "Odia (Oriya)",
            "om": "Oromo",
            "ps": "Pashto",
            "fa": "Persian",
            "pl": "Polish",
            "pt": "Portuguese (Portugal, Brazil)",
            "pa": "Punjabi",
            "qu": "Quechua",
            "ro": "Romanian",
            "ru": "Russian",
            "sm": "Samoan",
            "sa": "Sanskrit",
            "gd": "Scots Gaelic",
            "nso": "Sepedi",
            "sr": "Serbian",
            "st": "Sesotho",
            "sn": "Shona",
            "sd": "Sindhi",
            "si": "Sinhala (Sinhalese)",
            "sk": "Slovak",
            "sl": "Slovenian",
            "so": "Somali",
            "es": "Spanish",
            "su": "Sundanese",
            "sw": "Swahili",
            "sv": "Swedish",
            "tl": "Tagalog (Filipino)",
            "tg": "Tajik",
            "ta": "Tamil",
            "tt": "Tatar",
            "te": "Telugu",
            "th": "Thai",
            "ti": "Tigrinya",
            "ts": "Tsonga",
            "tr": "Turkish",
            "tk": "Turkmen",
            "ak": "Twi (Akan)",
            "uk": "Ukrainian",
            "ur": "Urdu",
            "ug": "Uyghur",
            "uz": "Uzbek",
            "vi": "Vietnamese",
            "cy": "Welsh",
            "xh": "Xhosa",
            "yi": "Yiddish",
            "yo": "Yoruba",
            "zu": "Zulu"

        }

    def update_file(self, url, keyword, languages):
        scraper = Scraper()
        self.logger.info(f'Scraping data from {url}...')
        last_post = scraper.get_page(url, keyword)
        self.logger.info(f'Done.')
        content = last_post['content']
        translator = Translator()
        images_root, feature_image_name = last_post['featured_image'].rsplit('/', 1)
        languages_to_translate = list(self.language_abbreviations.keys()) if languages in ['ALL', 'all', 'All'] else languages.split(',')

        for language_abbreviation in languages_to_translate:
            self.logger.info(f'Translating to {self.language_abbreviations[language_abbreviation]}...')
            try:
                soup = BeautifulSoup(content, 'lxml')
                translated_slug = translator.translate_dashed(last_post['slug'], language_abbreviation, romanize=True, uni=True)
                translated_title = translator.translate_string(last_post['title'], language_abbreviation)
                translated_seo_title = translator.translate_string(last_post['seo_title'], language_abbreviation)
                translated_seo_description = translator.translate_string(last_post['seo_description'], language_abbreviation)
                translated_keyword = translator.translate_string(last_post['keyword'], language_abbreviation, romanize=True)
                extension = '.' + feature_image_name.split('.')[-1]
                translated_featured_image = translator.translate_dashed(feature_image_name.replace(extension, ''), language_abbreviation, romanize=True, uni=True) + extension

                img_data = requests.get(last_post['featured_image']).content
                os.makedirs('data/featured/', exist_ok=True)
                with open('data/featured/' + translated_featured_image, 'wb') as handler:
                    handler.write(img_data)

                updated_featured_image = images_root + '/' + translated_featured_image
                translated_post_code = translator.translate_content(soup, language_abbreviation)

                this_translation = {
                    'slug': translated_slug,
                    'full_url': '?p=' + translated_slug,
                    'title': translated_title,
                    'seo_title': translated_seo_title,
                    'seo_description': translated_seo_description,
                    'keyword': translated_keyword,
                    'published_at': datetime.datetime.now().date(),
                    'featured_image': updated_featured_image,
                    'author': '',
                    'categories': last_post['categories'],
                    'excerpt': last_post['excerpt'],
                    'content': translated_post_code
                }
                this_translation_df = pd.DataFrame([this_translation])
                if not os.path.exists('data/output.csv'):
                    this_translation_df.to_csv('data/output.csv', mode='w', header=True, index=False)
                else:
                    this_translation_df.to_csv('data/output.csv', mode='a', header=False, index=False)
            except Exception as e:
                self.logger.error(f'{self.language_abbreviations[language_abbreviation]} FAILED: {e}. Continuing...')

            self.logger.info(f'Done.')
