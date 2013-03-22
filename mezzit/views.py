
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView

from mezzanine.conf import settings
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import paginate

from .models import Link
from .forms import LinkForm
from .utils import order_by_score


class ScoredView(ListView):

     def get_context_data(self, **kwargs):
        context = super(ScoredView, self).get_context_data(**kwargs)
        context["by_score"] = self.kwargs.get("by_score", True)
        try:
            username = self.kwargs["username"]
        except KeyError:
            context["profile_user"] = None
        else:
            users = User.objects.select_related("profile")
            user_lookup = {"username__iexact": username, "is_active": True}
            context["profile_user"] = get_object_or_404(users, **user_lookup)
        object_list = context.pop("object_list")
        if context["profile_user"]:
            object_list = object_list.filter(user=context["profile_user"])
        if context["by_score"]:
            object_list = order_by_score(object_list, self.date_field)
        else:
            object_list = object_list.order_by("-" + self.date_field)
        context["object_list"] = paginate(
            object_list,
            self.request.GET.get("page", 1),
            settings.ITEMS_PER_PAGE,
            settings.MAX_PAGING_LINKS,
        )
        context["title"] = self.get_title(context)
        return context


class LinkView(object):
    queryset = Link.objects.published().select_related("user", "user__profile")


class LinkList(LinkView, ScoredView):

    date_field = "publish_date"

    def get_title(self, context):
        if self.kwargs.get("by_score", True):
            return ""
        if context["profile_user"]:
            return "Links by %s" % context["profile_user"].profile
        else:
            return "Newest"

class LinkCreate(CreateView):

    form_class = LinkForm
    model = Link

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.gen_description = False
        return super(LinkCreate, self).form_valid(form)


class LinkDetail(LinkView, DetailView):
    pass


class CommentList(ScoredView):

    queryset = ThreadedComment.objects.visible() \
        .select_related("user", "user__profile") \
        .prefetch_related("content_object")
    date_field = "submit_date"

    def get_title(self, context):
        if context["profile_user"]:
            return "Comments by %s" % context["profile_user"].profile
        else:
            return "Latest comments"

