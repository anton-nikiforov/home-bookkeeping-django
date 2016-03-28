from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.safestring import mark_safe
from django.utils.encoding import (
    force_str, force_text, python_2_unicode_compatible,
)
from django.forms.utils import flatatt, to_current_timezone
from itertools import chain

from django.forms import SelectMultiple

class MultipleSearch(SelectMultiple):
	class Media:
		css = {
			'all' : ('css/hashtags.css',)
		}
		js = ('js/hashtags.js',)

	item_holder_html = u'''<div class="hashtags_widget" 
	data-search-url="{search}" data-create-url="{create}">
	<div class="form-group__tags">{tags}</div>
	<div class="btn-group btn-group__tags btn-group-justified">
		<div class="btn-group btn-group__large">
			<input type="text" value="" data-action="findTag" 
				autocomplete="off" class="form-control">
		</div>
		<div class="btn-group btn-group__small">
			<a class="btn btn-success glyphicon glyphicon-plus" 
				data-action="addTag" href="javascript:void(0);"></a>
		</div>
	</div>
	<div class="form-group__result"></div>
	<div class="form-group__list"></div></div>'''


	item_html = u'''<span class="label label-primary {id}" 
	data-hashtag="{pk}">{title}<a href="javascript:void(0);" 
	class="glyphicon glyphicon-remove"></a>{input}</span>'''

	search_url = None
	create_url = None

	def render(self, name, value, attrs=None, choices=()):
		if value is None:
			value = []
		final_attrs = self.build_attrs(attrs, type='hidden', name=name)
		id_ = final_attrs.get('id')
		inputs = []
		
		value = set(force_text(v) for v in value)

		for option_value, option_label in chain(self.choices, choices):
			option_value = force_text(option_value)
			if option_value in value:
				input_attrs = dict(value=option_value, **final_attrs)
				input_attrs['id'] = '%s_%s' % (id_, option_value)
				input_hidden = format_html('<input{} />', flatatt(input_attrs))

				inputs.append(format_html(self.item_html, id=input_attrs['id'],
					title=option_label, input=input_hidden, pk=option_value))
								
		return format_html(self.item_holder_html,
					tags=mark_safe('\n'.join(inputs)), search=self.search_url,
					create=self.create_url)