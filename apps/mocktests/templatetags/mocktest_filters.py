from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter
def to_letter(value):
    """Convert number to letter (0=A, 1=B, etc.)"""
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    try:
        idx = int(value)
        return letters[idx] if idx < len(letters) else chr(65 + idx)
    except (ValueError, TypeError):
        return str(value)


@register.filter
def to_json(value):
    """Convert Python object to JSON string"""
    return mark_safe(json.dumps(value))


@register.filter
def format_time(seconds):
    """Format seconds to MM:SS"""
    if not seconds:
        return "00:00"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


@register.simple_tag
def multiply(a, b):
    """Multiply two numbers"""
    try:
        return float(a) * float(b)
    except (ValueError, TypeError):
        return 0


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary"""
    return dictionary.get(key, "")
