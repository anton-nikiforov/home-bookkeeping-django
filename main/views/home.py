# -*- coding: utf-8 -*-
from django.shortcuts import render
from meta.views import Meta

from main.views import elements
from main.views.hashtags import get_summary_by_hashtags

def home(request):

	context = {
		'meta': Meta(**{'title': 'Home'}),
		'summary': elements.get_summary_by_category(),
		'summary_by_hashtags': get_summary_by_hashtags(20),
		'summary_by_year_month': elements.get_summary_by_year_month()
	}

	return render(request, "main/home.html", context)