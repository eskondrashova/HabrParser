import pandas as pd

from crawler import Crawler
from parser import Parser


def convert_to_excel(level, metas):
    df = pd.DataFrame(metas)

    writer = pd.ExcelWriter(f'{level}_vacancies.xlsx')
    df.to_excel(writer)
    writer.save()


if __name__ == '__main__':
    levels = {3: 'Junior',
              4: 'Middle',
              5: 'Senior'}
    for lev in levels:
        crawler = Crawler(lev)
        crawler.extract_urls()
        parser = Parser(crawler.urls)
        parser.parse()
        print(f'{levels[lev]}:\nКол-во вакансий: {len(parser.all_meta)}\nВакансии: {parser.all_meta}')
        convert_to_excel(levels[lev], parser.all_meta)
