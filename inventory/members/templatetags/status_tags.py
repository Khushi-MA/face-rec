from django import template

register = template.Library()

@register.filter(name='get_status_color')
def get_status_color(value):
    """Returns a Bootstrap color class based on percentage value."""
    try:
        percentage = float(value)
        if percentage > 85:
            return 'danger'  # High usage - red
        elif percentage > 70:
            return 'warning' # Moderate usage - yellow/orange
        else:
            return 'primary' # Normal usage - blue
    except (ValueError, TypeError):
        return 'secondary' # Default grey if value is not a valid number 