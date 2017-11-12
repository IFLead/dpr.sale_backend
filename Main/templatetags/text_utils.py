from django import template

register = template.Library()


@register.filter(name='reformat_title')
def reformat_title(title):
    if len(title) <= 20:
        return title
    else:
        return title[:17] + '...'
