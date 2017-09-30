"""Realtor URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from API import views
from Realtor import settings
from Realtor.settings import MEDIA_ROOT

urlpatterns = [
    url(r'districts/', views.districts),
    url(r'post/verify', views.verify_post),
    url(r'post/unverify', views.unverify_post),
    url(r'post/top', views.top_post),
    url(r'post/untop', views.untop_post),
    url(r'post/delete', views.delete_post),

    url(r'user/verify', views.verify_user),
    url(r'user/unverify', views.unverify_user),
]
