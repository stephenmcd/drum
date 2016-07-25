from __future__ import unicode_literals
from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = [
    url("^admin/", include(admin.site.urls)),
    url("^", include("drum.links.urls")),
    url("^", include("mezzanine.urls")),
]

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
