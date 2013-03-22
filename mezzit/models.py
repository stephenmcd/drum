
from time import time

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.core.models import Displayable, Ownable
from mezzanine.generic.models import Rating
from mezzanine.generic.fields import RatingField, CommentsField


class Link(Displayable, Ownable):

    link = models.URLField()
    rating = RatingField()
    comments = CommentsField()

    @models.permalink
    def get_absolute_url(self):
        return ("link_detail", (), {"slug": self.slug})


class Profile(models.Model):

    user = models.OneToOneField("auth.user")
    bio = models.TextField()
    karma = models.IntegerField(default=0, editable=False)


@receiver(post_save, sender=Rating)
def karma(sender, instance, **kwargs):
    """
    Each time a rating is saved, check its value and modify the
    profile karma for the related object's user accordingly.
    Since ratings are either +1/-1, if a rating is being edited,
    we can assume that the existing rating is in the other direction,
    so we multiply the karma modifier by 2.
    """
    value = int(instance.value)
    if not kwargs["created"]:
        value *= 2
    queryset = Profile.objects.filter(user=instance.content_object.user)
    queryset.update(karma=models.F("karma") + value)
