# In templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Custom filter to get an item from a dictionary by key."""
    return dictionary.get(key)



@register.filter
def to(value):
    """This filter returns a range from 1 to the given value."""
    return range(1, value + 1)
