from django import template

register = template.Library()

@register.filter
def break_after_n_chars(value, n):
    n = int(n)
    return '\n'.join([value[i:i+n] for i in range(0, len(value), n)])