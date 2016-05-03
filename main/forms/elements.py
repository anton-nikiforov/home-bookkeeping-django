# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML

from main.models import Elements, Hashtags
from main.forms.widgets import MultipleSearch
from main.helpers import reorder_fields

class ElementsCreateForm(forms.ModelForm):
	"""
		Create form
	"""
	created = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

	def __init__(self, *args, **kwargs):
		super(ElementsCreateForm, self).__init__(*args, **kwargs)

		for key, field in self.fields.iteritems():
			self.fields[key].widget.attrs['class'] = 'form-control'
		
		self.fields['created'].widget.attrs['class'] += ' daterange'

		self.fields['hashtags'].widget.search_url = reverse_lazy(
			'hashtags_search_ajax')

		self.fields['hashtags'].widget.create_url = reverse_lazy(
			'hashtags_create_ajax')

		self.fields['hashtags'].choices = {}

	class Meta:
		model = Elements
		fields = '__all__'
		widgets = {
			'hashtags': MultipleSearch
		}

class ElementsUpdateForm(ElementsCreateForm):
	"""
		Update form
	"""
	def __init__(self, *args, **kwargs):
		super(ElementsUpdateForm, self).__init__(*args, **kwargs)

		hashtags_initial = self.initial.get('hashtags', None)

		if hashtags_initial is not None:
			self.fields['hashtags'].choices = Hashtags.objects \
				.filter(id__in=hashtags_initial) \
				.values_list('id', 'title')

class ElementsFilterFormBase(forms.Form):
	"""
		Filter form
	"""
	is_exclude = forms.BooleanField(required=False, label='Exclude `Hashtags`')

	def __init__(self, *args, **kwargs):
		super(ElementsFilterFormBase, self).__init__(*args, **kwargs)

		self.fields = reorder_fields(self.fields, ['created', 'category',
									'hashtags', 'is_exclude'])

		self.helper = FormHelper(self)

		self.helper.form_action = 'javascript:void(0);'
		self.helper.form_method = 'GET'
		self.helper.help_text_inline = True
		self.helper.attrs = {'data_action': 'filter'}

		self.helper.layout.append(FormActions(
			Submit('', 'Search'),
			HTML(format_html("""
				<a class="reset_btn" href="{}">Reset</a>
			""", reverse_lazy('elements_list')))
		))

		if 'created' in self.fields:
			self.fields['created'].widget.attrs['class'] = 'daterange form-control'

		if 'hashtags' in self.fields:
			self.fields['hashtags'].choices = Hashtags.get_list()

	def exclude_hashtags(self):
		return self.is_valid() and 'is_exclude' in self.cleaned_data \
				and self.cleaned_data['is_exclude']