# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request, 'GTracker/index.html')

def others(request):
    return render(request, 'GTracker/others.html')
