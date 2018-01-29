from django.conf.urls import url

from . import views
import api
urlpatterns = [
    url(r'^$', views.grid, name='grid'),
    url(r'perspective/^$', views.perspective, name='perspective'),
    url(r'records/', api.records, name='records'),
]