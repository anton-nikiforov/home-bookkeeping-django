# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML

from main.models import Elements, Hashtags
from main.forms.widgets import MultipleSearch

class ElementsCreateForm(forms.ModelForm):
	created = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

	def __init__(self, *args, **kwargs):
		super(ElementsCreateForm, self).__init__(*args, **kwargs)

		for key, field in self.fields.iteritems():
			self.fields[key].widget.attrs['class'] = 'form-control'
		
		self.fields['created'].widget.attrs['class'] += ' daterange'

	class Meta:
		model = Elements
		fields = '__all__'
		widgets = {
			'hashtags': MultipleSearch
		}

class ElementsUpdateForm(ElementsCreateForm):
	
	def __init__(self, *args, **kwargs):
		super(ElementsUpdateForm, self).__init__(*args, **kwargs)
		hashtags_initial = self.initial.get('hashtags', None)

		if hashtags_initial is not None:
			self.fields['hashtags'].queryset = Hashtags.objects.filter(id__in=hashtags_initial)

class ElementsFilterFormBase(forms.Form):
	
	def __init__(self, *args, **kwargs):
		super(ElementsFilterFormBase, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		self.helper.form_action = 'javascript:void(0);'
		self.helper.form_method = 'GET'
		self.helper.help_text_inline = True
		self.helper.attrs = {'data_action': 'filter'}

		self.helper.layout.append(FormActions(
			Submit('', 'Search'),
		))

		self.fields['created'].widget.attrs['class'] = 'daterange form-control'