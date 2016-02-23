# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML

from ..models import Hashtags

class HashtagsCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(HashtagsCreateForm, self).__init__(*args, **kwargs)
	
		self.helper = FormHelper(self)

		self.helper.form_action = reverse_lazy('hashtags_create')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		self.helper.help_text_inline = True
		self.helper.label_class = 'col-sm-1 control-label'
		self.helper.field_class = 'col-sm-5'
		
		self.helper.layout.append(FormActions(
			Submit('save', 'Save'),
			HTML('<a class="btn btn-default" href="{}">{}</a>'.format(
				reverse_lazy('hashtags_list'),
				'Cancel'
			))
		))
		
	class Meta:
		model = Hashtags
		fields = '__all__'
		

class HashtagsUpdateForm(HashtagsCreateForm):
	def __init__(self, *args, **kwargs):
		super(HashtagsUpdateForm, self).__init__(*args, **kwargs)
		self.helper.form_action = reverse_lazy('hashtags_update', kwargs={'pk': kwargs['instance'].id})		
