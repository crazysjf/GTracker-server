from django.conf.urls import url

from . import views
import api
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'records/', api.records, name='records')
]