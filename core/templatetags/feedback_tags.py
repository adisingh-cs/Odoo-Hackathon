from django import template

register = template.Library()

@register.filter
def avg_rating(feedbacks):
    if feedbacks:
        return sum(f.rating for f in feedbacks) / len(feedbacks)
    return 0