from django import template
from newsletter.models import Newsletter, Edition

register = template.Library()

def do_get_latest_edition(parser, token):
    ''' Example usage: {% get_latest_edition for 'the-common' as newsletter %} '''

    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError, "get_next_events takes exactly five arguments"
    if bits[1] != 'for':
        raise template.TemplateSyntaxError, "second argument to the get_latest_newsletter tag must be 'for'"
    if bits[3] != 'as':
        raise template.TemplateSyntaxError, "fourth argument to the get_latest_newsletter tag must be 'as'"
    return GetLatestNewsletterNode(bits[2], bits[4])

class GetLatestNewsletterNode(template.Node):
    def __init__(self, slug, varname):
        self.slug, self.varname = slug, varname

    def render(self, context):
        try:
            context[self.varname] = Edition.objects.filter(newsletter__slug=self.slug).latest()
        except template.VariableDoesNotExist:
            context[self.varname] = ''
        return ''


register.tag("get_latest_edition", do_get_latest_edition)
