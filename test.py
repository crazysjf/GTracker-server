from celery import Celery
from crawler.db.db import DB, SortMethod
from pypinyin import lazy_pinyin
# db = DB()
# shops = db.get_all_shops()
# _shop = [''.join(lazy_pinyin(_[0])) for _ in shops]

#print _shop

sort_methods = [(_.param_str(), _.desc()) for _ in list(SortMethod)]

print sort_methods

print SortMethod.BY_SUM_SALES_7.param_str()