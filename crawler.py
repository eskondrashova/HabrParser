import numpy as np
import random
import requests

from time import sleep
from bs4 import BeautifulSoup as bs

from constants import HEADERS


class Crawler:
    """
    Crawler implementation
    """
    def __init__(self, qid):
        self.qid = qid
        self.pages = np.arange(1, 101, 1)
        self.urls = []

    def extract_urls(self):
        """
        Extracts urls
        """
        for page_num in self.pages:
            sleep(random.randint(1, 5))
            url = 'https://career.habr.com/vacancies?page=' + str(page_num) + '&qid=' + str(self.qid) + '&s[]=3&type=all'

            response = requests.get(url=url, headers=HEADERS)
            page_bs = bs(response.text, "html.parser")

            if page_bs.find('div', class_='no-content'):
                break
            else:
                self.urls.append(url)
                page_num += 1
