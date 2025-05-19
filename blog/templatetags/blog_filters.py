from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(is_safe=True)
def paragraphize(value):
    """
    Replaces double newlines with <p> tags and single newlines with <br />.
    """
    value = escape(value).replace('\n\n', '</p><p>')
    value = value.replace('\n', '<br />')
    value = '<p>%s</p>' % value
    return mark_safe(value)
