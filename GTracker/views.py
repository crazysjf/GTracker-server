# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import sys
from pypinyin import lazy_pinyin

from crawler.db.db import DB, SortMethod

# Create your views here.
def perspective(request):
    return render(request, 'GTracker/perspective.html')

def grid(request):
    # from GTracker.my_celery import debug_task
    # res = debug_task.delay(3, 4)
    # try:
    #     r = res.get(timeout=1)
    # except TimeoutError:
    db = DB()
    shops = db.get_all_shops()
    # 用拼音排序
    _shops = sorted(shops, key=lambda s:lazy_pinyin(s[0]))

    sort_methods = [(SortMethod.param_str(_), SortMethod.desc(_)) for _ in SortMethod.all()]
    return render(request, 'GTracker/grid.html', {'shops': _shops, 'sort_methods': sort_methods})

def others(request):
    return render(request, 'GTracker/others.html')

