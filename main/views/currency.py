# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpRequest

from ..forms import CurrencyCreateForm, CurrencyUpdateForm
from ..models import Currency
from views_json import JSONDeleteView, JSONFormView

from meta.views import MetadataMixin

class CurrencyListView(MetadataMixin, ListView):
	model = Currency
	title = 'Currencies'
	
	def get_context_data(self, **kwargs):
		context = super(CurrencyListView, self).get_context_data(**kwargs)
		currencies = context['currency_list']
		
		for currency in currencies:	
			setattr(currency, 'form_update', CurrencyUpdateForm(instance=currency, prefix=getattr(currency, 'id')))
			
		context['currency_list'] = currencies			
		context['form_create'] = CurrencyCreateForm
		
		return context
		
class CurrencyCreateView(JSONFormView, CreateView):
	model = Currency
	form_class = CurrencyCreateForm
	success_message = 'Created'
	success_url = reverse_lazy('currency_list')
	
	def get_context_data(self, **kwargs):
		context = super(CurrencyCreateView, self).get_context_data(**kwargs)
			
		return context
	
class CurrencyUpdateView(CurrencyCreateView, UpdateView):
	form_class = CurrencyUpdateForm
	success_message = 'Updated'
	
	def get_prefix(self):
		return self.kwargs['pk']
	
class JSONCurrencyDeleteView(JSONDeleteView):
	model = Currency
