from distutils.util import strtobool
import main
from datetime import datetime, timedelta, timezone
import re
from time import mktime
import env
from bs4 import BeautifulSoup, Tag


class RankingItem:

    def __init__(self, tag: Tag):

        # ページ構成変わったらここ変える
        self.rank = self.getText(tag.div.span.span).strip()
        self.path = tag.select_one('span > div > span > a').get('href').strip()
        self.title = self.getText(tag.select_one('span > a > div')).strip()
        self.star = self.getText(tag.select_one(
            'span > div.a-icon-row.a-spacing-none > a:nth-child(1)')).strip()
        self.reviewer = self.getText(tag.select_one(
            'span > div.a-icon-row.a-spacing-none > a:nth-child(2)')).strip()
        self.asin_isbn = re.search(
            r'\/dp\/.{10}', self.path).group()[4:]

        self.affUrl = "https://www.amazon.co.jp/dp/" + \
            self.asin_isbn+"/ref=nosim?tag=" + env.AFF_TAG

        # 文字数制限140文字なのでそれを超えないように大体50文字にtitleを丸める
        self.title = self.title[0:50]

    def __str__(self):
        return self.title

    def getText(self, tag: Tag) -> str:
        if tag == None:
            return ''
        return tag.text

    def shouldTweet(self) -> bool:
        if not self.isTweet:
            return False
        # １日以上過去の更新はツイートしない
        lastday = datetime.now(env.JST) + timedelta(days=-1)
        if self.published < lastday:
            return False
        if self.lastUpdate == None \
                or self.lastUpdate < self.published:
            return True
        return False

    def createTweetText(self) -> bool:
        text = '''
<Amazon>
にてお安く販売中！
お早目にチェックしてみてね！
#Amazon #アマゾン #お買い得
■商品名：{title}
■URL：{url}
［{date}]
'''.format(title=self.title, url=self.affUrl, date=self.published.strftime('%Y.%m.%d %H:%M:%S')).strip()
        print(text)
        print(len(text))
        return text
