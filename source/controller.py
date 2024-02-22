from bs4 import BeautifulSoup
import datetime

from tranlsator import Translator
import pandas as pd
import re


class Controller:
    def __init__(self, data_path):
        self.data_path = data_path
        self.csv_file = pd.read_csv('../data/posts_20240220.csv')

    def update_file(self):
        last_post = self.csv_file.iloc[-1]
        content = last_post['content']
        translator = Translator()
        language_abbreviations = ['af', 'in']

        images_root, feature_image_name = last_post['featured_image'].rsplit('/', 1)
        # language_abbreviations = ['de', 'es', 'fr', 'it', 'sr', 'br', 'ru', 'cn']

        new_content = pd.DataFrame(columns=self.csv_file.columns)
        for language_abbreviation in language_abbreviations:
            soup = BeautifulSoup(content, 'lxml')
            translated_slug = translator.translate_dashed(last_post['slug'], language_abbreviation)
            translated_slug = translator.translate_dashed(last_post['slug'], language_abbreviation)
            translated_title = translator.translate_string(last_post['title'], language_abbreviation)
            translated_seo_title = translator.translate_string(last_post['seo_title'], language_abbreviation)
            translated_seo_description = translator.translate_string(last_post['seo_description'], language_abbreviation)
            translated_keyword = translator.translate_string(last_post['keyword'], language_abbreviation)
            images_dir = images_root + '/' + language_abbreviation + '/'
            translated_featured_image = translator.translate_dashed(feature_image_name.replace('.png', ''), language_abbreviation)
            updated_featured_image = images_dir + translated_featured_image + '.png'





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
            new_content = pd.concat([new_content, this_translation_df], ignore_index=True)
        new_content.to_csv('../data/output.csv')
