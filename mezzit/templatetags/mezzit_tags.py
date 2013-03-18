
from collections import defaultdict
from django import template
from mezzanine.generic.models import ThreadedComment

from mezzit.utils import order_by_score


register = template.Library()


@register.simple_tag(takes_context=True)
def order_comments_by_score_for(context, parent):
    comments = defaultdict(list)
    comments_queryset = parent.comments.visible().select_related("user")
    for comment in order_by_score(comments_queryset, "submit_date"):
        comments[comment.replied_to_id].append(comment)
    context["all_comments"] = comments
    return ""
