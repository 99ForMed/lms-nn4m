from django import template

register = template.Library()

@register.filter(name = 'generate_range')
def generate_range(value):
    return range(value)