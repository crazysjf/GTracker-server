# -*- coding: utf-8 -*-
# 负责下载csv文件，检查哪些需要下载，并将下载的文件导入数据库。

import csv
import os
import re
from datetime import datetime, timedelta, date

from db import DB
import sqlite3

from crawler.misc.constants import *

# CSV_DIR = 'csv/'
# file_url_pattern = DZT_BASE_URL + 'member/items/all/%s/?t=all&act=out&d=%s'
#
# def download_one_file(driver, shop_id, date_str):
#     '''下载单个文件。'''
#     cookies = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
#     cookiestr = ';'.join(item for item in cookies)
#
#     file_url = file_url_pattern % (shop_id, date_str)
#     headers = {'cookie':cookiestr}
#     req = urllib2.Request(file_url, headers = headers)
#     try:
#         response = urllib2.urlopen(req)
#         text = response.read()
#
#         file_name = CSV_DIR + shop_id + '-' + date_str + '.csv'
#         fd = open(file_name, 'w')
#         fd.write(text)
#         fd.close()
#         print '###get %s success!!' % file_name
#     except:
#         print("Unexpected error:", sys.exc_info()[0])
#         raise

# def download_files(driver):
#     '''下载所有文件'''
#     if not os.path.exists(CSV_DIR):
#         os.makedirs(CSV_DIR)
#
#     shops = db.get_all_shops()
#
#     for shop in shops:
#         now = datetime.now()
#         for d in range(1,30):
#             delta = timedelta(days=d)
#             t = now - delta
#             date_str = t.strftime("%Y-%m-%d")
#
#             download_one_file(driver, shop[3], date_str)

def to_int(str):
    '''把str转为整数。如果成功返回整数，否则返回None'''
    try:
        return int(str)
    except:
        return None

GOOD_ID_PATTERN = re.compile(r'.*id=([0-9]*)$')
def get_good_id(link):
    '''从连接中获取商品ID'''
    m = GOOD_ID_PATTERN.match(link)
    if m == None:
        return None
    else:
        return m.group(1)


def import_to_db(shop_id, date, file, db_file=None):
    '''将csv文件导入数据库.
    date: datetime.date对象
    '''
    csv_reader = csv.reader(open(file, 'rb'))
    db = DB(db_file)
    for i, row in enumerate(csv_reader):
        if i == 0:
            continue
        # 所有元素解码
        try:
            _row = map(lambda x: x.decode('gb18030'), row)
        except Exception,e:
            print "row ", i, e
            continue

        title = _row[2]
        good_link = _row[3]
        creation_time = _row[4]
        view_cnt    = to_int(_row[6])
        fav_cnt     = to_int(_row[10])
        review_cnt  = to_int(_row[11])
        sales_30    = to_int(_row[12])

        good_id = get_good_id(good_link)
        # good_id没有就什么都不用做了
        if good_id == None:
            # 此处需要error log
            continue

        # 重复数据不用每次判断，直接插入，可以大幅提高性能
        # 如果重复会抛出IntegrityError异常，直接忽略即可。
        try:
            # if not db.good_exists(good_id):
            good = (title, shop_id, good_id, creation_time)
            db.insert_good(good)
        except sqlite3.IntegrityError as e:
            pass

        try:
            #if not db.record_exists(good_id, date):
            r = (date, good_id, sales_30, fav_cnt, view_cnt, review_cnt)
            db.insert_record(r)
        except sqlite3.IntegrityError as e:
            pass

    db.commit()

def import_files_in_dir(dir, db_file=None):
    files =  os.listdir(dir)
    p = re.compile(r'([0-9]*)-([0-9,-]*).csv')
    db = DB(db_file)
    for f in files:
        m = p.match(f)
        shop_id =  m.group(1)
        date = datetime.strptime(m.group(2), '%Y-%m-%d').date()
        import_to_db(shop_id, date, dir + f)
        print 'imported: ' + f
        db.commit()
    db.finish()

if __name__ == "__main__":
    pass
