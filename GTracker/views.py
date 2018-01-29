# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def perspective(request):
    return render(request, 'GTracker/perspective.html')

def grid(request):
    from GTracker.my_celery import debug_task
    res = debug_task.delay(3, 4)
    # try:
    #     r = res.get(timeout=1)
    # except TimeoutError:

    return render(request, 'GTracker/grid.html')

def others(request):
    return render(request, 'GTracker/others.html')
