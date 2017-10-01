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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from Main import views
from Realtor import settings
from Realtor.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^dash/', views.dashboard),
    url(r'^send_request/', views.new_post),
    url(r'^sign_up/', views.sign_up),
    url(r'^api/', include('API.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^(?P<post_id>\d+)/$', views.post_view, name='post_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
