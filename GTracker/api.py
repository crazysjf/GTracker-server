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


def records(request):
    db.init(db_path)
    rs = db.get_records3('162545180')
    result = {}
    for r in rs:
        good_id     = r[0]
        sales_30    = r[1]
        v = []
        if result.has_key(good_id):
            v = result[good_id]
        else:
            result[good_id] = v
        v.append(sales_30)

    array =[]
    for key in result.keys():
        d = {}
        d['text'] = key
        d['values'] = result[key]
        array.append(d)
    return HttpResponse(json.dumps(array, cls=DjangoJSONEncoder), content_type="application/json")
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