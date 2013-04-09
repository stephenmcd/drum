
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
from .models import Link


admin.site.register(Link, DisplayableAdmin)
