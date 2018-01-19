# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def perspective(request):
    return render(request, 'GTracker/perspective.html')

def grid(request):
    return render(request, 'GTracker/grid.html')

def others(request):
    return render(request, 'GTracker/others.html')
