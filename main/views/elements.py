# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from main.forms.elements import ElementsCreateForm, ElementsUpdateForm
from main.models.elements import Elements

from meta.views import MetadataMixin

class ElementsListView(MetadataMixin, ListView):
	model = Elements
	title = 'Records'

	def get_context_data(self, **kwargs):
		context = super(ElementsListView, self).get_context_data(**kwargs)
		context['elements'] = Elements.objects.all()

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
