from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key, 0)
    except (AttributeError, TypeError):
        return 0


@register.filter
def duration_format(minutes):
    """Convert minutes to hours and minutes format"""
    try:
        minutes = int(minutes)
        if minutes >= 60:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}m"
        return f"{minutes}min"
    except (ValueError, TypeError):
        return "0min"
