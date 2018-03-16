from django.conf.urls import url

from . import views
import api
urlpatterns = [
    url(r'^$', views.grid, name='grid'),
    url(r'perspective/^$', views.perspective, name='perspective'),
    url(r'goods_nr/', api.goods_nr, name='goods_nr'),
    url(r'records/', api.records, name='records'),
]