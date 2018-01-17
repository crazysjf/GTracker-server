# -*- coding: utf-8 -*-
import sys
db_path = "../GTracker-crawler/"
sys.path.append(db_path)
from django.shortcuts import render
import logging
logger = logging.getLogger("django")
import db
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date, datetime, timedelta


def records(request):
    global  date
    db.init(db_path)
    shop_id = request.GET.get('shop_id',"")

    date_range = 30
    # 获取指定shop_id的30内所有记录
    end_date = date.today()
    start_date = end_date - timedelta(date_range)
    rs = db.get_records_with_shop_id_in_date_range(shop_id, start_date, end_date)
    result = {}

    for r in rs:
        good_id     = r[0]
        date        = datetime.strptime(r[1],'%Y-%m-%d').date()
        sales_30    = r[2]
        good_data = {}
        if result.has_key(good_id):
            good_data = result[good_id]
        else:
            good_data['sales_30'] = [100] * (date_range + 1)
            result[good_id] = good_data
        idx = (date - start_date).days
        good_data['sales_30'][idx] = sales_30

    # _r = {}
    # for i,k in enumerate(result.keys()):
    #     if i < 5:
    #         _r[k] = result[k]
    #     else:
    #         break
    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder), content_type="application/json")
    # eName           = request.GET.get('employee',"")
    # startDateStr       = request.GET.get('startDate', "")
    # endDateStr         = request.GET.get('endDate', "")
    # ucode           = request.GET.get('ucode', "")
    #
    # startDate = 0
    # endDate = 0
    # #e = Employee.objects.get(name_text = eName)
    # if startDateStr == "" or endDateStr == "":
    #     startDate = now().date()
    #     endDate = startDate + timedelta(days=1)
    # else:
    #     startDate = datetime.strptime(startDateStr, '%Y-%m-%d')
    #     endDate = datetime.strptime(endDateStr + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    #
    # objs = Record.objects
    # if ucode != "" :
    #     objs = objs.filter(ucode_text__exact = ucode)
    #
    # if eName != "":
    #     objs = objs.filter(employee__name_text = eName)
    #
    # rs = objs.filter(datetime__range=(startDate, endDate)).order_by("-datetime")
    #
    # #rs  = e.record_set.filter(datetime__range=(start, end)).order_by("-datetime")
    # employeeList = []
    # ucodeList = []
    # datetimeList = []
    # for r in rs:
    #     employeeList.append(r.employee.name_text)
    #     ucodeList.append(r.ucode_text)
    #     datetimeList.append(r.datetime)
    # a = {}
    # a['employeeList']   = employeeList
    # a['ucodeList']       = ucodeList
    # a['datetimeList']   = datetimeList
    #
    # return HttpResponse(json.dumps(a, cls=DjangoJSONEncoder), content_type="application/json")v