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
from django.contrib import admin

from API import views

urlpatterns = [
	# url(r'districts/', views.districts),
	# url(r'post/verify', views.verify_post),
	# url(r'post/unverify', views.unverify_post),
	# url(r'post/top', views.top_post),
	# url(r'post/untop', views.untop_post),
	# url(r'post/close', views.close_post),
	# url(r'post/restore', views.restore_post),
	# url(r'post/delete', views.delete_post),
	# url(r'post/edit', views.edit_post),
	# url(r'post/important', views.important_post),
	# url(r'post/unimportant', views.unimportant_post),
	# url(r'post/get_top_eight', views.get_top_eight),
	url(r'^admin/', admin.site.urls),
	url(r'currency', views.CurrencyList.as_view(), name='currency list'),
	url(r'categories', views.CategoryList.as_view(), name='categories list'),
	url(r'posts', views.PostList.as_view(), name='post list'),
	url(r'(?P<pk>\d+)/$', views.PostDetail.as_view(), name='detail'),
	url(r'(?P<pk>\d+)/edit/', views.PostUpdate.as_view(), name='update'),
	url(r'(?P<pk>\d+)/delete/', views.PostDestroy.as_view(), name='destroy'),
	url(r'create/', views.PostCreate.as_view(), name='create'),

	# url(r'user/verify', views.verify_user),
	# url(r'user/unverify', views.unverify_user),
	# url(r'user/edit', views.edit_profile),
	#
	# url(r'search', views.search),
	# url(r'more', views.more),
]
