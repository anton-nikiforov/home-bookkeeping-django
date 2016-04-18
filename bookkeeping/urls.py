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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import logout

from main.views import home, hashtags, currency, category, elements, auth
from import_app.views import import_view

urlpatterns = [
	url(regex=r'^$', view=home, name='home'),
	
	url(regex=r'^hashtags/$', view=hashtags.HashtagsListView.as_view(), name='hashtags_list'),
	url(regex=r'^hashtags/create/$', view=hashtags.HashtagsCreateView.as_view(), name='hashtags_create'),
	url(regex=r'^hashtags/(?P<pk>\d+)/$', view=hashtags.HashtagsUpdateView.as_view(), name='hashtags_update'),
	url(regex=r'^hashtags/delete/(?P<pk>\d+)/$', view=hashtags.HashtagsDeleteView.as_view(), name='hashtags_delete'),
	url(regex=r'^hashtags/delete/(?P<pk>\d+)/ajax/$', view=hashtags.JSONHashtagsDeleteView.as_view(), name='hashtags_delete_ajax'),
	url(regex=r'^hashtags/search/ajax/$', view=hashtags.JSONHashtagsSearchView.as_view(), name='hashtags_search_ajax'),
	url(regex=r'^hashtags/create/ajax/$', view=hashtags.JSONHashtagsCreateView.as_view(), name='hashtags_create_ajax'),

	url(regex=r'^currency/$', view=currency.CurrencyListView.as_view(), name='currency_list'),
	url(regex=r'^currency/create/ajax/$', view=currency.CurrencyCreateView.as_view(), name='currency_create_ajax'),
	url(regex=r'^currency/(?P<pk>\d+)/ajax/$', view=currency.CurrencyUpdateView.as_view(), name='currency_update_ajax'),
	url(regex=r'^currency/delete/(?P<pk>\d+)/ajax/$', view=currency.JSONCurrencyDeleteView.as_view(), name='currency_delete_ajax'),
	
	url(regex=r'^category/$', view=category.CategoryListView.as_view(), name='category_list'),
	url(regex=r'^category/create/ajax/$', view=category.CategoryCreateView.as_view(), name='category_create_ajax'),
	url(regex=r'^category/(?P<pk>\d+)/ajax/$', view=category.CategoryUpdateView.as_view(), name='category_update_ajax'),
	url(regex=r'^category/delete/(?P<pk>\d+)/ajax/$', view=category.JSONCategoryDeleteView.as_view(), name='category_delete_ajax'),	

	url(regex=r'^elements/$', view=elements.elements_list, name='elements_list'),
	url(regex=r'^elements/filter/(?P<filter_url>.+)/$', view=elements.elements_list, name='elements_list_filter'),	
	url(regex=r'^elements/create/$', view=elements.ElementsCreateView.as_view(), name='elements_create'),
	url(regex=r'^elements/(?P<pk>\d+)/$', view=elements.ElementsUpdateView.as_view(), name='elements_update'),
	url(regex=r'^elements/delete/(?P<pk>\d+)/$', view=elements.ElementsDeleteView.as_view(), name='elements_delete'),

	url(regex=r'^import/$', view=import_view, name='import_view'),

	#url('^accounts/', include('django.contrib.auth.urls')),
	url(r'^accounts/login/$', auth.login, name='login'),
	url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
	url(r'^admin/', include(admin.site.urls)),
]