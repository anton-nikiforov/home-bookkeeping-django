from django import template

register = template.Library()
	
@register.simple_tag(takes_context=True)
def is_active(context, urlname):
    if context['request'].resolver_match.url_name in urlname:
        return 'active'
    return ''
	
@register.filter(name='split')
def split(value, arg):
    return value.split(arg)