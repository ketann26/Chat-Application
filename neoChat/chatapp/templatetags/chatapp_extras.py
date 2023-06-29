from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.simple_tag
def construct_url(id1,id2):
    if(id1<id2):
        return 'chat-{}-{}'.format(str(id1),str(id2))
    else:
        return 'chat-{}-{}'.format(str(id2),str(id1))