from django import template

register = template.Library()

@register.filter(stringformat=True)
def currency(value):
    return "${:,.2f}".format(value)
