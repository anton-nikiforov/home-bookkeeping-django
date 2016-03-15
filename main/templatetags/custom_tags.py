from django.template import Library, Node, resolve_variable

register = Library()
	
@register.simple_tag(takes_context=True)
def is_active(context, urlname):
    if context['request'].resolver_match.url_name in urlname:
        return 'active'
    return ''

@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

class AddGetParameter(Node):
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = resolve_variable('request', context)
        params = req.GET.copy()
        for key, value in self.values.items():
            params[key] = value.resolve(context)
        return '?%s' %  params.urlencode()


@register.tag
def add_get(parser, token):
    pairs = token.split_contents()[1:]
    values = {}
    for pair in pairs:
        s = pair.split('=', 1)
        values[s[0]] = parser.compile_filter(s[1])
    return AddGetParameter(values)