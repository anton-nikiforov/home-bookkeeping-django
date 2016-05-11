# -*- coding: utf-8 -*-
from django.db.models import Sum
from django.template.loader import render_to_string
from django.http import Http404
from django.http.request import QueryDict, MultiValueDict
from django.contrib import messages
from django.views.generic import (
	ListView, CreateView, UpdateView, DeleteView
)
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import (
	Paginator, EmptyPage, PageNotAnInteger
)
from django.shortcuts import render
from django import forms

from main.forms import (
	ElementsCreateForm, ElementsUpdateForm, ElementsFilterFormBase
)
from main.models import Elements, Hashtags

from meta.views import MetadataMixin
from meta.views import Meta

import django_filters

class ElementsFilter(django_filters.FilterSet):
	"""
		Filter component class for Elements
	"""
	created = django_filters.DateFromToRangeFilter()
	hashtags = django_filters.MultipleChoiceFilter(widget=forms.CheckboxSelectMultiple())

	def __init__(self, data=None, queryset=None, prefix=None, strict=None):
		super(ElementsFilter, self).__init__(data, queryset, prefix, strict)
		if self.form.exclude_hashtags():
			self.filters['hashtags'].exclude=True

	class Meta:
		model = Elements
		form = ElementsFilterFormBase
		fields = ['created', 'category', 'hashtags']

def elements_list(request, filter_url=None):
	"""
		Try to make semantic url for filter.
		TODO make it DRY
	"""
	filter_data = {}
	
	if filter_url:
		for part in filter_url.split(';'):
			params = part.split('-is-')
			try:
				items = params[1].split('-or-')
			except:
				raise Http404("Url does not exist.")
			filter_data[params[0]] = items
			
	qdict = QueryDict('', mutable=True)
	qdict.update(MultiValueDict(filter_data))			
	element_qs = Elements.objects.all().order_by('-created', 'total')

	f = ElementsFilter(data=qdict or request.GET, queryset=element_qs)

	paginator = Paginator(f.qs, 17)
	page = request.GET.get('page')
	try:
		page = paginator.page(page)
	except PageNotAnInteger:
		page = paginator.page(1)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)

	context = {
		'filter': f,
		'meta': Meta(**{'title': 'Records'}),
		'paginator': paginator,
		'page_obj': page,
		'is_paginated': page.has_other_pages(),
		'cache_key': f.qs._cache_key(),
		'summary': get_summary_by_category(f.qs)
	}

	return render(request, 'main/elements_list_filter.html', context)

class ElementsCreateView(MetadataMixin, CreateView):
	model = Elements
	form_class = ElementsCreateForm
	success_message = 'Created'
	success_url = reverse_lazy('elements_list')
	title = 'Create record'

	def get_context_data(self, **kwargs):
		context = super(ElementsCreateView, self).get_context_data(**kwargs)
		context['hashtags_top'] = Hashtags.get_list(limit=21)
		return context

	def form_valid(self, form):
		messages.success(self.request, self.success_message, extra_tags='msg')
		return super(ElementsCreateView, self).form_valid(form)			
	
class ElementsUpdateView(ElementsCreateView, UpdateView):
	form_class = ElementsUpdateForm
	success_message = 'Updated'

	def get_meta_title(self, context):
		return 'Update record "{0}"'.format(self.get_object())	
	
class ElementsDeleteView(MetadataMixin, DeleteView):
	model = Elements
	success_url = reverse_lazy('elements_list')
	success_message = 'Deleted'
	
	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(ElementsDeleteView, self).delete(request, *args, **kwargs)	
		
	def get_meta_title(self, context):
		return 'Delete record "{0}"'.format(self.get_object())	


def get_summary_by_category(queryset=None):
	"""
		Summary grouped by category and currency
	"""
	try:
		if queryset is None:
			queryset = Elements.objects.all()
		summary = queryset \
			.values('category__title', 'currency__symbol') \
			.annotate(sum=Sum('total')).order_by('sum')
	except:
		summary = None
	if summary:
		return render_to_string("main/get_summary_by_category.html", {
			'summary': summary
			})
	return False

def get_summary_by_year_month():
	"""
		Summary grouped by year, month, category and currency
	"""
	try:
		summary = Elements.objects \
			.extra(select={
				'created_year': 'date_format(created, "%%Y")',
				'created_month_order': 'date_format(created, "%%m")',
				'created_month': 'date_format(created, "%%M")'}) \
			.values('created_year', 'created_month', 
					'category__title', 'currency__symbol') \
			.annotate(sum=Sum('total')) \
			.order_by('-created_year', '-created_month_order')
	except:
		summary = None
	if summary:
		return render_to_string("main/get_summary_by_year_month.html", {
			'summary': summary
			})
	return False
