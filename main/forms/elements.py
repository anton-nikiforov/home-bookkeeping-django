# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML

from main.models.elements import Elements

class ElementsCreateForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(ElementsCreateForm, self).__init__(*args, **kwargs)

		for key, field in self.fields.iteritems():
			self.fields[key].widget.attrs['class'] = 'form-control'
		
	class Meta:
		model = Elements
		fields = '__all__'		

class ElementsUpdateForm(ElementsCreateForm):
	def __init__(self, *args, **kwargs):
		super(ElementsUpdateForm, self).__init__(*args, **kwargs)		
