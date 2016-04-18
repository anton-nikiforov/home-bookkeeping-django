# -*- coding: utf-8 -*-
from django.shortcuts import render
from meta.views import Meta

from main.views.elements import get_summary_by_category
from main.views.hashtags import get_summary_by_hashtags

def home(request):

	context = {
		'meta': Meta(**{'title': 'Home'}),
		'summary': get_summary_by_category(),
		'summary_by_hashtags': get_summary_by_hashtags(20)
	}

	return render(request, "main/home.html", context)