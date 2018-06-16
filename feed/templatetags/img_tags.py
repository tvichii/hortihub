from django import template

register = template.Library()

@register.filter
def get_type(value):
    t = type(value)
    return t.__name__
