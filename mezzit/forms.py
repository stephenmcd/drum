
from django.forms import ModelForm
from mezzit.models import Link


class LinkForm(ModelForm):

    class Meta:
        model = Link
        fields = ("title", "link", "description")
