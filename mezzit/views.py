
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from mezzanine.conf import settings
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import render, paginate

from .models import Link
from .forms import LinkForm


PAGING = (settings.ITEMS_PER_PAGE, settings.MAX_PAGING_LINKS)


def link_detail(request, slug, template="link_detail.html"):
    context = {"link": get_object_or_404(Link, slug=slug)}
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


@login_required
def link_edit(request, slug, template="link_form.html"):
    queryset = Link.objects.published(for_user=request.user)
    link = get_object_or_404(queryset, slug=slug)
    link_form = LinkForm(request.POST or None, instance=link)
    if request.method == "POST" and link_form.is_valid():
        link = link_form.save()
        return redirect(link)
    context = {"link_form": link_form}
    return render(request, template, context)


def link_list(request, template="link_list.html"):
    page = request.GET.get("page", 1)
    links = paginate(Link.objects.all(), page, *PAGING)
    context = {"links": links}
    return render(request, template, context)


def user_links(request, username, template="user_links.html"):
    profile_user = get_object_or_404(User, username__iexact=username,
                                     is_active=True)
    page = request.GET.get("page", 1)
    links = Link.objects.filter(user=profile_user)
    links = paginate(links.order_by("-publish_date"), page, *PAGING)
    context = {"links": links, "profile_user": profile_user}
    return render(request, template, context)


def user_comments(request, username, template="user_comments.html"):
    profile_user = get_object_or_404(User, username__iexact=username,
                                     is_active=True)
    page = request.GET.get("page", 1)
    comments = ThreadedComment.objects.filter(user=profile_user)
    comments = paginate(comments.order_by("-submit_date"), page, *PAGING)
    context = {"comments": comments, "profile_user": profile_user}
    return render(request, template, context)
