
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
from .models import Link


class LinkAdmin(DisplayableAdmin):

    list_display = ("id", "title", "link", "status", "publish_date",
                    "user", "comments_count", "rating_sum")
    list_display_links = ("id",)
    list_editable = ("title", "link", "status")
    list_filter = ("status", "user__username")
    ordering = ("-publish_date",)

    fieldsets = (
        (None, {
            "fields": ("title", "link", "status", "publish_date", "user"),
        }),
    )


admin.site.register(Link, LinkAdmin)
