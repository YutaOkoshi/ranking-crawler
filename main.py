from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from distutils.util import strtobool
import requests
import time
from bs4 import BeautifulSoup, Tag

import env
from model.ranking import Ranking
from model.category import Category
from model.amazon_category import AmazonCategory

# ------------ GSpreadSheet周り
ApiScope = ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']
Credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'secure.json', ApiScope)
GspreadClient = gspread.authorize(Credentials)
SpreadSheet = GspreadClient.open(env.SPREADSHEET_NAME)


def getTargetCategory() -> list[Category]:
    MainSheet = SpreadSheet.worksheet(env.MAINSHEET_NAME)
    MainList = MainSheet.get_all_values()
    MainList.pop(0)
    MainList.pop(0)
    res = []
    # print(MainList)
    for item in MainList:
        # 「有効か」列が有効で存在するカテゴリーなこと
        if strtobool(item[2]) \
                and AmazonCategory.has_enum(item[0]):
            res += [Category(item)]
    return res


def updateTargetCategory(category: str):
    MainSheet = SpreadSheet.worksheet(env.MAINSHEET_NAME)
    cell = MainSheet.find(query=category, in_row=0)
    now = datetime.now(env.JST).strftime('%Y/%m/%d %H:%M:%S')
    # E列が「データの最終更新日時」の前提
    MainSheet.update_cell(cell.address[1:], 5, now)
    pass


def main(event, context):

    categories = getTargetCategory()

    for category in categories:

        if not category.shouldCrawl():
            print("{} is not target".format(category))
            continue

        ranking = crawl(str(category))
        ranking.toCsv()
        # if env.IS_PRD:
        if ranking.saveBucket():
            updateTargetCategory(str(category))
            pass


def crawl(category: str) -> Ranking:
    time.sleep(3)
    headers = {
        "User-Agent": env.UA
    }
    url = 'https://www.amazon.co.jp/gp/bestsellers/'+category
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        body = BeautifulSoup(r.text, 'lxml')
        ranking = Ranking(category, body)
        return ranking
    return None
