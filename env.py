from datetime import timedelta, timezone
import os
from os.path import join, dirname
from dotenv import load_dotenv

import os


if os.getenv("ENV") == "PRD":
    print('is production mode')
    IS_PRD = True
else:
    IS_PRD = False

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

JST = timezone(timedelta(hours=+9), 'JST')

#------------ スプレットシート周り
SPREADSHEET_NAME = os.environ.get('SPREADSHEET_NAME')
MAINSHEET_NAME = os.environ.get('MAINSHEET_NAME')

#------------ アフェリエイトURL用のタグ
AFF_TAG = os.environ.get('AFF_TAG')

#------------ スプレイピング周り
UA = os.environ.get('UA')

#------------ GCP周り
# ローカルから実行するときはCredentialsで認証する
if not IS_PRD:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './secure.json'
BUCKET_NAME = os.environ.get('BUCKET_NAME')
