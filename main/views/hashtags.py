# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.generic import (
	ListView, CreateView, UpdateView, DeleteView, View
)
from django.core.urlresolvers import reverse_lazy

from braces.views import JSONResponseMixin
from meta.views import MetadataMixin

from ..forms import HashtagsCreateForm, HashtagsUpdateForm
from ..models import Hashtags
from views_json import JSONDeleteView

from django.core.cache import cache

class HashtagsListView(MetadataMixin, ListView):
	title = 'Hashtags'
	paginate_by = 15

	def get_queryset(self):
		return Hashtags.objects.all().order_by('title')
	
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
		
class JSONHashtagsSearchView(JSONResponseMixin, View):
	"""
		Search in create/update views
		Recieve request from hashtags.js
	"""
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):

		title = request.POST.get('tag', None)

		response = {
			u'action': False,
			u'tag': title
		}

		if title is not None:
			queryset = Hashtags.objects.filter(title__startswith=title)
			hashtag_ids = request.POST.getlist('choosen[]', None)
			hashtags_list = {}

			if hashtag_ids is not None:
				queryset = queryset.exclude(pk__in=hashtag_ids)

				response.update({'choosen': hashtag_ids})

			for hashtag in queryset:
				hashtags_list[hashtag.pk] = {
					'id': hashtag.pk,
					'title': hashtag.title	
				}

			response.update({
				u'action': True, 
				'hashtags': hashtags_list
			})

		return self.render_json_response(response)

class JSONHashtagsCreateView(JSONResponseMixin, View):
	"""
		Create new hashtag in create/update views
		Recieve request from hashtags.js
	"""
	http_method_names = ['post']

	def post(self, request, *args, **kwargs):

		title = request.POST.get('tag', None)

		response = {
			u'action': False,
			u'tag': title
		}

		if title is None:
			response.update({
				'message': 'Hashtag is required.'	
			})
		else:
			try:
				hashtag = Hashtags(title=title)
				hashtag.save()
				
				response.update({
					u'action': True,
					'ID': hashtag.id,
					'info': {}
				})

				response['info'][hashtag.id] = {
					'id': hashtag.id,
					u'title': hashtag.title
				}
			except Exception, e:
				response.update({
					'message': str(e)
				})

		return self.render_json_response(response)

def get_summary_by_hashtags(limit=None):
	"""
		Summary and count grouped by hashtags
	"""
	from django.db.models import Sum, Count
	summary = Hashtags.objects.all() \
		.values('title', 'elements__currency__symbol') \
		.annotate(count=Count('elements__id')) \
		.annotate(sum=Sum('elements__total')) \
		.order_by('-count')
	if limit is not None:
		summary = summary[:limit]
	context = {
		'summary': summary
	}

	return render_to_string("main/get_summary_by_hashtags.html", context)	