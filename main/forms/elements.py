# -*- coding: utf-8 -*-
from django import forms

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
	pass

class ElementsFilterFormBase(forms.Form):
	
	def __init__(self, *args, **kwargs):
		super(ElementsFilterFormBase, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		self.helper.form_method = 'GET'
		#self.helper.form_class = 'form-horizontal'

		self.helper.help_text_inline = True
		#self.helper.label_class = 'col-sm-12'
		#self.helper.field_class = 'col-sm-12'
		
		self.helper.layout.append(FormActions(
			Submit('', 'Search'),
		))

		#self.fields['created'].widget.attrs['class']# = 'daterangefilter'