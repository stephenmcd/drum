
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("mezzit.views",
    url("^$", "link_list",
        name="home"),
    url("^newest/$", "link_list", {"by_score": False},
        name="link_list_latest"),
    url("^comments/$", "comment_list",
        name="comment_list_latest"),
    url("^link/create/$", "link_create",
        name="link_create"),
    url("^link/(?P<slug>.*)/$", "link_detail",
        name="link_detail"),
    url("^users/(?P<username>.*)/links/$", "link_list", {"by_score": False},
        name="link_list_user"),
    url("^users/(?P<username>.*)/comments/$", "comment_list",
        name="comment_list_user"),
)
