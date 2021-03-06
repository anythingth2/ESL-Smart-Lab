"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.http import HttpRequest
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
import views
import sqlite3
import os



urlpatterns = [
    url(r'^dashboard', views.dashboard),
    url(r'^controller', views.controller),
    url(r'^member', views.member),
    url(r'^historyTable', views.historyTable),
    url(r'^login',views.login),
    url(r'^openDoorNow',views.instant_open_door),
    url(r'^reqDoorPassword',views.generate_door_password),
    url(r'^test',views.memberTable),
    url(r'^memberTable',views.memberTable),
    url(r'^addMember',views.add_member),
    url(r'^open_door',views.open_door),
    # url("", views.socket),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
