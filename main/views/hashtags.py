# -*- coding: utf-8 -*-
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from ..forms import HashtagsCreateForm, HashtagsUpdateForm
from ..models import Hashtags
from views_json import JSONDeleteView

from meta.views import MetadataMixin

class HashtagsListView(MetadataMixin, ListView):
	model = Hashtags
	title = 'Hashtags'
	
class HashtagsCreateView(MetadataMixin, CreateView):
	model = Hashtags
	success_url = reverse_lazy('hashtags_list')
	success_message = 'Created'
	title = 'Create hashtag'
	form_class = HashtagsCreateForm
	
	def form_valid(self, form):
		messages.success(self.request, self.success_message, extra_tags='msg')
		return super(HashtagsCreateView, self).form_valid(form)	

class HashtagsUpdateView(HashtagsCreateView, UpdateView):
	success_message = 'Updated'
	form_class = HashtagsUpdateForm
	
	def get_meta_title(self, context):
		return 'Update hashtag "{0}"'.format(self.get_object())
	
class HashtagsDeleteView(MetadataMixin, DeleteView):
	model = Hashtags
	success_url = reverse_lazy('hashtags_list')
	success_message = 'Deleted'
	
	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(HashtagsDeleteView, self).delete(request, *args, **kwargs)	
		
	def get_meta_title(self, context):
		return 'Delete hashtag "{0}"'.format(self.get_object())		
		
class JSONHashtagsDeleteView(JSONDeleteView):
	model = Hashtags
		
		