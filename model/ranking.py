from datetime import datetime
import env
from bs4 import BeautifulSoup
from model.ranking_item import RankingItem
import csv
from google.cloud import storage


class Ranking:

    items = []
    category = ''

    def __init__(self, category: str, bs: BeautifulSoup):
        Ranking.items = []
        Ranking.category = category
        # ページ構成変わったらここ変える
        list = bs.select('ol#zg-ordered-list > li > span > div')
        for li in list:
            Ranking.items += [RankingItem(li)]

    def getItem(self) -> list[RankingItem]:
        return Ranking.items

    def toCsv(self) -> bool:

        # CloudFunctionsで書き込み可能な部分は /tmp ディレクトリだけです。
        # https://cloud.google.com/functions/docs/concepts/exec?hl=ja#file_system
        filename = '{}.csv'.format(Ranking.category)
        if env.IS_PRD:
            filename = '/tmp/' + filename

        with open(filename, 'w', newline='') as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL)
            header = ['rank', 'asin_isbn', 'title', 'star',
                      'reviewer', 'affUrl', 'path']
            w.writerow(header)
            for item in self.getItem():
                w.writerow([
                    item.rank,
                    item.asin_isbn,
                    item.title,
                    item.star,
                    item.reviewer,
                    item.affUrl,
                    item.path,
                ])
        return True

    def saveBucket(self) -> bool:

        client = storage.Client()
        bucket = client.get_bucket(env.BUCKET_NAME)

        filename = '{}.csv'.format(Ranking.category)
        if env.IS_PRD:
            filename = '/tmp/' + filename

        now = datetime.now(env.JST)

        blob = bucket.blob('{}/{}/{}/{}/{}.csv'.format(
            now.year, now.month, now.day, now.hour, Ranking.category))
        blob.upload_from_filename(filename=filename)
        return True
