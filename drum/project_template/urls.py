from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    ("^", include("drum.links.urls")),
    ("^", include("mezzanine.urls")),
)

# Adds ``STATIC_URL`` to the context.
handler500 = "mezzanine.core.views.server_error"
