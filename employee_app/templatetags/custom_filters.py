from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Safely get a value from a dictionary in templates.
    Usage: {{ my_dict|get_item:key_var }}
    """
    return dictionary.get(key)