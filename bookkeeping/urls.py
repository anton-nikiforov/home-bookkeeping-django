"""bookkeeping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

from main import views

urlpatterns = [
	url(regex=r'^$', view=views.home, name='home'),
	url(regex=r'^hashtags/$', view=views.HashtagsListView.as_view(), name='hashtags_list'),
	url(regex=r'^hashtags/create/$', view=views.HashtagsCreateView.as_view(), name='hashtags_create'),
	url(regex=r'^hashtags/(?P<pk>\d+)/$', view=views.HashtagsUpdateView.as_view(), name='hashtags_update'),
	url(regex=r'^hashtags/delete/(?P<pk>\d+)/$', view=views.HashtagsDeleteView.as_view(), name='hashtags_delete'),
	url(regex=r'^hashtags/delete/(?P<pk>\d+)/ajax/$', view=views.JSONHashtagsDeleteView.as_view(), name='hashtags_delete_ajax'),
	url(regex=r'^currency/$', view=views.CurrencyListView.as_view(), name='currency_list'),
	url(regex=r'^currency/create/ajax/$', view=views.CurrencyCreateView.as_view(), name='currency_create_ajax'),
	url(regex=r'^currency/(?P<pk>\d+)/ajax/$', view=views.CurrencyUpdateView.as_view(), name='currency_update_ajax'),
	url(regex=r'^currency/delete/(?P<pk>\d+)/ajax/$', view=views.JSONCurrencyDeleteView.as_view(), name='currency_delete_ajax'),
	url(regex=r'^category/$', view=views.CategoryListView.as_view(), name='category_list'),
	url(regex=r'^category/create/ajax/$', view=views.CategoryCreateView.as_view(), name='category_create_ajax'),
	url(regex=r'^category/(?P<pk>\d+)/ajax/$', view=views.CategoryUpdateView.as_view(), name='category_update_ajax'),
	url(regex=r'^category/delete/(?P<pk>\d+)/ajax/$', view=views.JSONCategoryDeleteView.as_view(), name='category_delete_ajax'),	
	url(r'^admin/', include(admin.site.urls)),
]