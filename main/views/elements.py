# -*- coding: utf-8 -*-
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
from django.db.models import Sum, Count

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

	class Meta:
		model = Elements
		form = ElementsFilterFormBase
		fields = ['created', 'category', 'hashtags']
		#order_by = ['-created', 'total', '-total']

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

	f = ElementsFilter(qdict or request.GET, queryset=Elements.objects.all() \
		.select_related('currency', 'category').prefetch_related('hashtags') \
		.order_by('-created', 'total'))

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
		'elements_list': page.object_list,
		'summary': f.qs.values('category__title', 'currency__symbol') \
						.annotate(sum=Sum('total')).order_by('sum')
	}

	return render(request, 'main/elements_list_filter.html', context)

class ElementsListView(MetadataMixin, ListView):
	'''
		Deprecated view for records list
	'''
	title = 'Records'
	model = Elements
	paginate_by = 15

	def get_queryset(self):
		return Elements.objects.all().select_related('currency', 'category') \
				.prefetch_related('hashtags').order_by('-created')


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
