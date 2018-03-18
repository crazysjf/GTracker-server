# -*- coding: utf-8 -*-
import sys
db_path = "../GTracker-crawler/"
sys.path.append(db_path)
from django.shortcuts import render
import logging
logger = logging.getLogger("django")
from crawler.db.db import DB, SortMethod
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date, datetime, timedelta
from crawler.network.dzt_crawler import DztCrawler as Crawler
from django.template.loader import render_to_string
from common.utils import gen_diff, str_2_date

def goods_nr(request):
    global date
    db = DB()
    shop_id = request.GET.get('shop_id', "")
    if shop_id == 'null':
        shop_id = None
    goods_nr = db.get_goods_nr(shop_id)
    return HttpResponse(json.dumps({'goods_nr': goods_nr}, cls=DjangoJSONEncoder), content_type="application/json")


def records(request):
    global date
    db = DB()
    shop_id = request.GET.get('shop_id', "")
    if shop_id == 'null':
        shop_id = None
    sm_str = request.GET.get('sort', "SumSales3")
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 200)

    date_range = 30
    # 获取指定shop_id的30内所有记录
    end_date = date.today() - timedelta(1)  # 结束日期最多到昨天
    start_date = end_date - timedelta(date_range)  # 包括start_date和end_date在内共date_range + 1天

    sm = SortMethod.param_str_2_sort_method(sm_str)
    goods = db.get_goods(shop_id, sm, offset, limit)

    # result格式
    # [
    #  {gid: <good_id_1>, sales: [d11, d12, ...], name: <good-name>, main_pic:<主图>, shop_name:<店铺名称>, create:<创建时间>},
    #  {gid: <good_id_2>, sales: [d21, d22,...],  name: <good-name>, main_pic:<主图>, shop_name:<店铺名称>, create:<创建时间>}
    # ]
    result = []

    for g in goods:
        gid = g[0]
        rs = db.get_records_with_good_id_in_date_range(gid, start_date, end_date)
        a = [None] * ((end_date - start_date).days + 1)
        for r in rs:
            idx = (str_2_date(r[0]) - start_date).days
            a[idx] = r[1]

        sales = gen_diff(a)

        d = {}
        d['gid']        = gid
        d['name']       = g[1]
        d['main_pic']   = g[2]
        d['create']     = g[3]
        d['sales']      = sales
        shop_id = g[4]
        shop_name = db.get_shop_name(shop_id)
        d['shop_name']  = shop_name
        result.append(d)


    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder), content_type="application/json")


def need_log_in(request):
    f = Crawler.need_log_in_flag()
    return HttpResponse(json.dumps(f, cls=DjangoJSONEncoder), content_type="application/json")

def log_in_frag(request):
    
    html = render_to_string("GTracker/need_log_in_frag.html")
    return HttpResponse(json.dumps(html, cls=DjangoJSONEncoder), content_type="application/json")
