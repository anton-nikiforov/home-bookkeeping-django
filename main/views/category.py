# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpRequest

from ..forms import CategoryCreateForm, CategoryUpdateForm
from ..models import Category
from views_json import JSONDeleteView, JSONFormView

from meta.views import MetadataMixin

class CategoryListView(MetadataMixin, ListView):
	model = Category
	title = 'Categories'
	
	def get_context_data(self, **kwargs):
		context = super(CategoryListView, self).get_context_data(**kwargs)
		categories = context['category_list'] 
		
		for category in categories:	
			setattr(category, 'form_update', CategoryUpdateForm(instance=category, prefix=getattr(category, 'id')))
			
		context['category_list'] = categories			
		context['form_create'] = CategoryCreateForm
		
		return context
		
class CategoryCreateView(JSONFormView, CreateView):
	model = Category
	form_class = CategoryCreateForm
	success_message = 'Created'
	success_url = reverse_lazy('category_list')
	
	def get_context_data(self, **kwargs):
		context = super(CategoryCreateView, self).get_context_data(**kwargs)
			
		return context
	
class CategoryUpdateView(CategoryCreateView, UpdateView):
	form_class = CategoryUpdateForm
	success_message = 'Updated'
	
	def get_prefix(self):
		return self.kwargs['pk']
	
class JSONCategoryDeleteView(JSONDeleteView):
	model = Category
