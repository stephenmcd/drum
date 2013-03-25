
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView

from mezzanine.conf import settings
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import paginate

from .models import Link
from .forms import LinkForm
from .utils import order_by_score


class UserFilterView(ListView):
    """
    List view that puts a ``profile_user`` variable into the context,
    which is optionally retrieved by a ``username`` urlpattern var.
    If a user is loaded, ``object_list`` is filtered by the loaded
    user. Used for showing lists of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(UserFilterView, self).get_context_data(**kwargs)
        try:
            username = self.kwargs["username"]
        except KeyError:
            profile_user = None
        else:
            users = User.objects.select_related("profile")
            lookup = {"username__iexact": username, "is_active": True}
            profile_user = get_object_or_404(users, **lookup)
            object_list = context["object_list"].filter(user=profile_user)
            context["object_list"] = object_list
        context["profile_user"] = profile_user
        return context


class ScoreOrderingView(UserFilterView):
    """
    List view that optionally orders ``object_list`` by calculated
    score. Subclasses must defined a ``date_field`` attribute for the
    related model, that's used to determine time-scaled scoring.
    Ordering by score is the default behaviour, but can be
    overridden by passing ``False`` to the ``by_score`` arg in
    urlpatterns, in which case ``object_list`` is sorted by most
    recent, using the ``date_field`` attribute. Used for showing lists
    of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(ScoreOrderingView, self).get_context_data(**kwargs)
        object_list = context["object_list"]
        context["by_score"] = self.kwargs.get("by_score", True)
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
    """
    List and detail view mixin for links - just defines the correct
    queryset.
    """
    queryset = Link.objects.published().select_related("user", "user__profile")


class LinkList(LinkView, ScoreOrderingView):
    """
    List view for links, which can be for all users (homepage) or
    a single user (links from user's profile page). Links can be
    order by score (homepage, profile links) or by most recently
    created ("newest" main nav item).
    """

    date_field = "publish_date"

    def get_title(self, context):
        if self.kwargs.get("by_score", True):
            return ""
        if context["profile_user"]:
            return "Links by %s" % context["profile_user"].profile
        else:
            return "Newest"


class LinkCreate(CreateView):
    """
    Link creation view - assigns the user to the new link, as well
    as setting Mezzanine's ``gen_description`` attribute to ``False``,
    so that we can provide our own descriptions.
    """

    form_class = LinkForm
    model = Link

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.gen_description = False
        return super(LinkCreate, self).form_valid(form)


class LinkDetail(LinkView, DetailView):
    """
    Link detail view - threaded comments and rating are implemented
    in its template.
    """
    pass


class CommentList(ScoreOrderingView):
    """
    List view for comments, which can be for all users ("comments" and
    "best" main nav items) or a single user (comments from user's
    profile page). Comments can be order by score ("best" main nav item)
    or by most recently created ("comments" main nav item, profile
    comments).
    """

    queryset = ThreadedComment.objects.visible() \
        .select_related("user", "user__profile") \
        .prefetch_related("content_object")
    date_field = "submit_date"

    def get_title(self, context):
        if context["profile_user"]:
            return "Comments by %s" % context["profile_user"].profile
        else:
            return "Latest comments"

