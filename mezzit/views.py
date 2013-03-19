

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from mezzanine.conf import settings
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import render, paginate

from .models import Link
from .forms import LinkForm
from .utils import order_by_score


PAGING = (settings.ITEMS_PER_PAGE, settings.MAX_PAGING_LINKS)


def link_detail(request, slug, template="link_detail.html"):
    links = Link.objects.select_related("user")
    context = {"link": get_object_or_404(links, slug=slug)}
    return render(request, template, context)


@login_required
def link_create(request, template="link_form.html"):
    link_form = LinkForm(request.POST or None)
    if request.method == "POST" and link_form.is_valid():
        link = link_form.save(commit=False)
        link.user = request.user
        link.gen_description = False
        link.save()
        return redirect(link)
    context = {"link_form": link_form}
    return render(request, template, context)


def link_list(request, username=None, by_score=True, template="link_list.html"):
    links = Link.objects.select_related("user")
    profile_user = None
    title = ""
    if username:
        user_lookup = {"username__iexact": username, "is_active": True}
        profile_user = get_object_or_404(User, **user_lookup)
        links = links.filter(user=profile_user)
    if by_score:
        links = order_by_score(links, "publish_date")
    else:
        links = links.order_by("-publish_date")
        if profile_user:
            title = "Links for %s" % profile_user
        else:
            title = "Newest"
    context = {
        "links": paginate(links, request.GET.get("page", 1), *PAGING),
        "profile_user": profile_user,
        "title": title,
    }
    return render(request, template, context)


def comment_list(request, username=None, template="comment_list.html"):
    comments = ThreadedComment.objects.select_related("user")
    profile_user = None
    title = "Latest comments"
    if username:
        user_lookup = {"username__iexact": username, "is_active": True}
        profile_user = get_object_or_404(User, **user_lookup)
        comments = comments.filter(user=profile_user)
        title = "Comments for %s" % profile_user
    comments = comments.order_by("-submit_date")
    context = {
        "comments": paginate(comments, request.GET.get("page", 1), *PAGING),
        "profile_user": profile_user,
        "title": title,
    }
    return render(request, template, context)
