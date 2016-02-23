# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML

from ..models import Currency

class CurrencyCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CurrencyCreateForm, self).__init__(*args, **kwargs)
	
		self.helper = FormHelper(self)

		self.helper.form_action = reverse_lazy('currency_create_ajax')
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
		
		try:
			base_currency_id = Currency.objects.filter(base=1)[0].id
		except:
			base_currency_id = 0
		
		pk = kwargs['instance'].id if 'instance' in kwargs and hasattr(kwargs['instance'], 'id') else 0
			
		if base_currency_id and base_currency_id != pk:
			self.fields['base'].widget.attrs['disabled'] = True
		
	class Meta:
		model = Currency
		fields = '__all__'
		

class CurrencyUpdateForm(CurrencyCreateForm):
	def __init__(self, *args, **kwargs):
		super(CurrencyUpdateForm, self).__init__(*args, **kwargs)
		self.helper.form_action = reverse_lazy('currency_update_ajax', kwargs={'pk': kwargs['instance'].id})