# -*- coding: utf-8 -*-
from django.http import Http404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from main.forms import ElementsCreateForm, ElementsUpdateForm, ElementsFilterFormBase
from main.models.elements import Elements

from meta.views import MetadataMixin
from meta.views import Meta

import django_filters

class ElementsFilter(django_filters.FilterSet):
	created = django_filters.DateFromToRangeFilter()

	class Meta:
		model = Elements
		form = ElementsFilterFormBase
		fields = ['created', 'category', 'hashtags']
		order_by = ['-created', 'total', '-total']

def elements_list(request):
    f = ElementsFilter(request.GET, queryset=Elements.objects.all().select_related('currency', 'category').prefetch_related('hashtags').order_by('-created'))

    paginator = Paginator(f.qs, 15)
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
        'elements_list': page.object_list
    }

    return render(request, 'main/elements_list_filter.html', context)

class ElementsListView(MetadataMixin, ListView):
	title = 'Records'
	model = Elements
	paginate_by = 15

	def dispatch(self, *args, **kwargs):
		"""
		filter_uri = self.kwargs.get('filter')

		if filter_uri:
			self.kwargs['filter_data'] = {}
			filter_data = filter_uri.split(';')

			for parts in filter_data:
				part = parts.split('=')

				if len(part) != 2 or hasattr(self.model, part[0]) == False:
					raise Http404("Field does not exist.")

				self.kwargs['filter_data'][part[0]] = part[1].split('-')
		"""
		return super(ElementsListView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		return Elements.objects.all().select_related('currency', 'category').prefetch_related('hashtags').order_by('-created')

	def get_context_data(self, **kwargs):
		context = super(ElementsListView, self).get_context_data(**kwargs)
		"""
		if self.kwargs.get('filter_data'):
			context['filter_data'] = self.kwargs.get('filter_data')
		"""
		return context


class ElementsCreateView(MetadataMixin, CreateView):
	model = Elements
	form_class = ElementsCreateForm
	success_message = 'Created'
	success_url = reverse_lazy('elements_list')
	title = 'Create record'
	
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
