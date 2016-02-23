# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML

from ..models import Category

class CategoryCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CategoryCreateForm, self).__init__(*args, **kwargs)
	
		self.helper = FormHelper(self)

		self.helper.form_action = reverse_lazy('category_create_ajax')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		self.helper.attrs = {'data_action': 'create'}

		self.helper.help_text_inline = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		
		self.helper.layout.append(FormActions(
			Submit('save', 'Save'),
			HTML('<button class="btn btn-default" data-dismiss="modal">{}</button>'.format(
				'Cancel'
			))
		))
		
	class Meta:
		model = Category
		fields = '__all__'
		

class CategoryUpdateForm(CategoryCreateForm):
	def __init__(self, *args, **kwargs):
		super(CategoryUpdateForm, self).__init__(*args, **kwargs)
		self.helper.form_action = reverse_lazy('category_update_ajax', kwargs={'pk': kwargs['instance'].id})