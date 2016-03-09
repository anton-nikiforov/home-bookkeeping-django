# -*- coding: utf-8 -*-
from django.shortcuts import render
from meta.views import Meta

def home(request):
	return render(request, "main/home.html", {'meta': Meta(**{'title': 'Main'})})