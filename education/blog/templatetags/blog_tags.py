from django import template
from ..models import Comment

register = template.Library()


@register.filter(name='getReplies')
def getReplies(comment):
    return Comment.objects.filter(parent=comment)
