"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
import GTracker.views
import GTracker.api

urlpatterns = [
    url(r'^$', GTracker.views.grid),
    url(r'^grid/$', GTracker.views.grid),
    url(r'^perspective/$', GTracker.views.perspective),

    url(r'others/', GTracker.views.others),

    url(r'^GTracker/', include('GTracker.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'api/records/', GTracker.api.records, name='records'),
    url(r'api/need_log_in/', GTracker.api.need_log_in, name='need_log_in'),
    url(r'api/log_in_frag/', GTracker.api.log_in_frag, name='log_in_frag'),
]
