import datetime
import random
import requests

from time import sleep
from bs4 import BeautifulSoup as bs

from constants import HEADERS


class Parser:
    """
    Parser implementation
    """
    def __init__(self, page_urls):
        self.page_urls = page_urls

        self.vacancy_name = ''
        self.vacancy_link = ''
        self.publication_date = ''
        self.company_name = ''
        self.salary = ''
        self.employee_skills = ''
        self.workplace = ''

        self.all_meta = []

    def parse(self):
        """
        Extracts all necessary data from web page
        """
        for url in self.page_urls:
            response = requests.get(url=url, headers=HEADERS)
            sleep(random.randint(1, 5))
            page_bs = bs(response.text, 'html.parser')
            content_bs = page_bs.find_all('div', class_='vacancy-card__inner')
            for vacancy_bs in content_bs:
                vacancy_info = vacancy_bs.find('div', class_='vacancy-card__info')
                self._get_vacancy_name(vacancy_info)
                self._get_vacancy_link(vacancy_bs)
                self._get_publication_date(vacancy_bs)
                self._get_company_name(vacancy_info)
                self._get_salary(vacancy_info)
                self._get_employee_skills(vacancy_info)
                self._get_place_name(vacancy_info)
                self.all_meta.append(self._get_meta())
        return self.all_meta

    def _get_vacancy_name(self, vacancy_info):
        vacancy_name = vacancy_info.find('div', class_='vacancy-card__title')
        self.vacancy_name = vacancy_name.text

    def _get_vacancy_link(self, vacancy_bs):
        raw_link = vacancy_bs.find('a').get('href')
        link = 'https://career.habr.com' + raw_link
        self.vacancy_link = link

    def _get_publication_date(self, vacancy_bs):
        raw_date = vacancy_bs.find('time', class_='basic-date').get('datetime')
        publication_date = datetime.datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S+03:00')
        self.publication_date = str(publication_date)

    def _get_company_name(self, vacancy_info):
        company_name = vacancy_info.find('div', class_='vacancy-card__company-title')
        self.company_name = company_name.text

    def _get_salary(self, vacancy_info):
        salary = vacancy_info.find('div', class_='basic-salary')
        self.salary = salary.text

    def _get_employee_skills(self, vacancy_info):
        raw_skills = vacancy_info.find('div', class_='vacancy-card__skills')
        skills = raw_skills.text.split(' • ')
        self.employee_skills = ', '.join(skills)

    def _get_place_name(self, vacancy_bs):
        vacancy_meta = vacancy_bs.find('div', class_='vacancy-card__meta')
        cities = vacancy_meta.find_all('a', class_='link-comp link-comp--appearance-dark')
        cities_list = []
        for city in cities:
            cities_list.append(city.text)
        self.workplace = ', '.join(cities_list)

    def _get_meta(self):
        vacancy_dict = {
            'name': self.vacancy_name,
            'link': self.vacancy_link,
            'published': self.publication_date,
            'company': self.company_name,
            'salary': self.salary,
            'required_skills': self.employee_skills,
            'cities': self.workplace
        }
        return vacancy_dict
