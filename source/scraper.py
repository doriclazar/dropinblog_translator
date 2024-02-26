import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class Scraper:
    def __init__(self):
        self._create_driver()

    def _create_driver(self):
        options = Options()

        options.add_argument('--headless')

        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--accept-encoding=gzip, deflate, br')
        options.add_argument('--scheme=https')
        options.add_argument('--sec-ch-ua=".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"')
        options.add_argument('--sec-ch-ua-mobile=?0')
        options.add_argument('--sec-ch-ua-platform="Windows"')
        options.add_argument('--sec-fetch-dest=document')
        options.add_argument('--sec-fetch-mode=navigate')
        options.add_argument('--sec-fetch-site=none')
        options.add_argument('--sec-fetch-user=?1')
        options.add_argument('--upgrade-insecure-requests=1')
        options.add_argument('--accept-language=en-US,en;q=0.9')
        options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/'
                             'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
        options.add_argument('start-maximized')
        options.add_argument("--enable-javascript")
        options.add_argument("--log-output=NULL")

        self.driver = webdriver.Chrome(
            options=options,
            service=Service(ChromeDriverManager().install(), log_output='NUL'))
        self.driver.set_window_size(3840, 2160)

    def get_page(self, url, keyword):
        self.driver.get(url)
        results = {
            'slug': url.split('?p=')[1],
            'full_url': url,
            'title': self.driver.find_element(By.TAG_NAME, 'title').get_attribute('text'),
            'seo_title': self.driver.find_element(By.XPATH, '//meta[@property = "og:title"]').get_attribute('content'),
            'seo_description': self.driver.find_element(By.XPATH, '//meta[@property = "og:description"]').get_attribute('content'),
            'keyword': keyword,
            'published_at': datetime.datetime.now().date(),
            'featured_image': self.driver.find_element(By.XPATH, '//meta[@property = "og:image"]').get_attribute('content'),
            'author': '',
            'categories': self.driver.find_element(By.XPATH, '//span[contains(@class, "dib-post-category-text")]').text,
            'excerpt': '',
            'content': self.driver.find_element(By.XPATH, '//div[contains(@class, "dib-post-content")]').get_attribute('innerHTML').replace('\n    ', '').replace('\n', '')
        }
        self.driver.close()
        return results
