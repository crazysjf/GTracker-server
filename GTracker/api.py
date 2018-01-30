# -*- coding: utf-8 -*-
import sys
db_path = "../GTracker-crawler/"
sys.path.append(db_path)
from django.shortcuts import render
import logging
logger = logging.getLogger("django")
from db.db import DB
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date, datetime, timedelta
from network.dzt_crawler import DztCrawler as Crawler
from django.template.loader import render_to_string

# def gen_diff(a):
#     '''
#     计算数组a的差分并返回。
#     a中允许有None存在。
#     返回数组的长度比a的长度小1。
#     '''
#     def remove_none(a):
#         '''去掉数组a里面的None：如果第一个值为None，则替换为0，如果不是第一个值为None，则替换为结果数组里面的前一个值'''
#         r = [0] * len(a)
#         for i in range(0, len(a)):
#             if a[i] == None:
#                  r[i] = 0 if i == 0 else r[i-1]
#             else:
#                 r[i] = a[i]
#         return r
#     b = remove_none(a)
#     c = [b[i] - b[i-1] for i,x in enumerate(b) if i > 0]
#     return c

def gen_diff(a):
    '''
    计算数组a的差分并返回。
    a中允许有None存在.
    返回数组的长度比a的长度小1。
    假设返回值为r:
    如果a[i] == None, 则r[i] = None；
    如果a[i] != None，则r[i] = a[i]和最近一个非空值的差。
    如果a[0] == None则当0处理
    
    [1, 2, 3]    => [1, 1]
    [1, None, 3] => [None, 2]
    [None, 2, 3] => [2, 1]
    [None, None, 3] => [None, 3]
    '''
    r = [None] * (len(a) - 1)
    last_unnone = 0 if a[0] == None else a[0] # 最近一个非None值
    for i in range(1, len(a)):
        if a[i] == None:
            r[i-1] = None
        else:
            if a[i - 1] == None:
                r[i-1] = a[i] - last_unnone
            else:
                r[i-1] = a[i] - a[i-1]
            last_unnone = a[i]
    return r


def records(request):
    global  date
    db = DB()
    shop_id = request.GET.get('shop_id',"")

    date_range = 30
    # 获取指定shop_id的30内所有记录
    end_date = date.today()
    start_date = end_date - timedelta(date_range - 1)
    rs = db.get_records_with_shop_id_in_date_range(shop_id, start_date, end_date)

    # result格式
    # {
    #  <good_id_1>: {sales_30: [d11, d12, ...], name: <good-name>},
    #  <good_id_2>: {sales_30: [d21, d22,...],  name: <good-name>}
    # }
    result = {}

    for r in rs:
        good_id     = r[0]
        date        = datetime.strptime(r[1],'%Y-%m-%d').date()
        sales_30    = r[2]
        good_name   = r[3]
        good_data = {}
        if result.has_key(good_id):
            good_data = result[good_id]
        else:
            good_data['sales_30'] = [None] * (date_range + 1)
            good_data['name'] = good_name
            result[good_id] = good_data
        idx = (date - start_date).days
        good_data['sales_30'][idx] = sales_30

    for good_id in result.keys():
        good_data = result[good_id]
        good_data['sales'] = gen_diff(good_data['sales_30'])
        good_data.pop('sales_30')   # 无需30天销量

    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder), content_type="application/json")


def need_log_in(request):
    f = Crawler.need_log_in_flag()
    return HttpResponse(json.dumps(f, cls=DjangoJSONEncoder), content_type="application/json")

def log_in_frag(request):
    
    html = render_to_string("GTracker/need_log_in_frag.html")
    return HttpResponse(json.dumps(html, cls=DjangoJSONEncoder), content_type="application/json")
