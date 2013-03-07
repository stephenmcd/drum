
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from mezzanine.conf import settings
from mezzanine.utils.views import render, paginate

from .models import Link
from .forms import LinkForm


def link_detail(request, slug):
    link = get_object_or_404(Link, slug=slug)
    return render(request, "link_detail.html", {"link": link})


@login_required
def link_create(request):
    link_form = LinkForm(request.POST or None)
    if request.method == "POST" and link_form.is_valid():
        link = link_form.save(commit=False)
        link.user = request.user
        link.gen_description = False
        link.save()
        return redirect(link)
    return render(request, "link_form.html", {"link_form": link_form})


@login_required
def link_edit(request, slug):
    queryset = Link.objects.published(for_user=request.user)
    link = get_object_or_404(queryset, slug=slug)
    link_form = LinkForm(request.POST or None, instance=link)
    if request.method == "POST" and link_form.is_valid():
        link = link_form.save()
        return redirect(link)
    return render(request, "link_form.html", {"link_form": link_form})


def link_list(request):
    page = request.GET.get("page", 1)
    per_page = 20
    max_links = settings.MAX_PAGING_LINKS
    links = paginate(Link.objects.all(), page, per_page, max_links)
    return render(request, "link_list.html", {"links": links})


