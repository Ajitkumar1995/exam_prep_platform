from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    try:
        return dictionary.get(key, 0)
    except (AttributeError, TypeError):
        return 0


@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def get_range(value):
    """Return a range of numbers"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)
