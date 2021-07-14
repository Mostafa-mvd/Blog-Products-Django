from django import template

register = template.Library()


@register.filter
def jdate(value, my_format="%Y-%m-%d"):
    return value.strftime(my_format)
