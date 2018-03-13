# -*- coding: utf-8 -*-
import sys
db_path = "../GTracker-crawler/"
sys.path.append(db_path)
from django.shortcuts import render
import logging
logger = logging.getLogger("django")
from crawler.db.db import DB
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date, datetime, timedelta
from crawler.network.dzt_crawler import DztCrawler as Crawler
from django.template.loader import render_to_string
from common.utils import gen_diff2

def records(request):
    global  date
    db = DB()
    shop_id = request.GET.get('shop_id',"")

    date_range = 30
    # 获取指定shop_id的30内所有记录
    end_date = date.today() - timedelta(1) # 结束日期最多到昨天
    start_date = end_date - timedelta(date_range)     # 包括start_date和end_date在内共date_range + 1天
    rs = db.get_records_with_shop_id_in_date_range(shop_id, start_date, end_date)

    # result格式
    # [
    #  {gid: <good_id_1>, sales: [d11, d12, ...], name: <good-name>, main_pic:<主图>, shop_name:<店铺名称>, create:<创建时间>},
    #  {gid: <good_id_2>, sales: [d21, d22,...],  name: <good-name>, main_pic:<主图>, shop_name:<店铺名称>, create:<创建时间>}
    # ]
    result = {}

    for r in rs:
        good_id     = r[0]
        date        = datetime.strptime(r[1],'%Y-%m-%d').date()
        bid30    = r[2]
        good_name   = r[3]
        good_data = {}
        if result.has_key(good_id):
            good_data = result[good_id]
        else:
            good_data['bid30'] = [None] * (date_range + 1)
            good_data['name'] = good_name
            g_info = db.get_good_info(good_id)
            shop_name = db.get_shop_name(shop_id)
            good_data['main_pic'] = g_info[3]
            good_data['create'] = g_info[2].split()[0] # 只返回日期部分，不返回时间
            good_data['shop_name'] = shop_name
            result[good_id] = good_data
        idx = (date - start_date).days
        good_data['bid30'][idx] = bid30

    _result = []

    for good_id in result.keys():
        good_data = result[good_id]
        good_data['sales'] = gen_diff2(good_data['bid30'])
        good_data.pop('bid30')   # 无需30天销量
        good_data['gid'] = good_id
        _result.append(good_data)


    # 排序
    def sum_of_last_3_days(good):
        sales = good['sales']
        return sales[-1] + sales[-2] + sales[-3]
    re = sorted(_result, key=sum_of_last_3_days, reverse=True)

    # debug
    for r in re:
        if r['gid'] == '546849050764':
            print r

    return HttpResponse(json.dumps(re, cls=DjangoJSONEncoder), content_type="application/json")


def need_log_in(request):
    f = Crawler.need_log_in_flag()
    return HttpResponse(json.dumps(f, cls=DjangoJSONEncoder), content_type="application/json")

def log_in_frag(request):
    
    html = render_to_string("GTracker/need_log_in_frag.html")
    return HttpResponse(json.dumps(html, cls=DjangoJSONEncoder), content_type="application/json")
