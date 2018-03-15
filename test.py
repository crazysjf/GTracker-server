from celery import Celery
from crawler.db.db import DB
from pypinyin import lazy_pinyin
db = DB()
shops = db.get_all_shops()
_shop = [''.join(lazy_pinyin(_[0])) for _ in shops]

print _shop