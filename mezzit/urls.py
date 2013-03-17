
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("mezzit.views",
    url("^$", "link_list", name="home"),
    url("^newest/$", "link_list", {"by_score": False}, name="latest_links"),
    #url("^comments/$", "comments", name="latest_comments"),
    url("^link/create/$", "link_create", name="link_create"),
    url("^link/(?P<slug>.*)/edit/$", "link_edit", name="link_edit"),
    url("^link/(?P<slug>.*)/$", "link_detail", name="link_detail"),
    url("^users/(?P<username>.*)/comments/$", "user_comments",
        name="user_comments"),
    url("^users/(?P<username>.*)/links/$", "user_links",
        name="user_links"),
)
