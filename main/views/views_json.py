# -*- coding: utf-8 -*-
from braces.views import JSONResponseMixin

from django.views.generic import DeleteView

class JSONDeleteView(JSONResponseMixin, DeleteView):
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return self.render_json_response({u'action': True, u'message': 'Deleted'})
		
class JSONFormView(JSONResponseMixin):
	def form_valid(self, form):
		response = super(JSONFormView, self).form_valid(form)
		return self.render_json_response({u'action': True, u'message': self.success_message, u'pk': self.object.pk})
		
	def form_invalid(self, form):
		response = super(JSONFormView, self).form_invalid(form)
		return self.render_json_response({u'action': False, u'form': response.rendered_content})		
