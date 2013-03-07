
from django.db import models
from mezzanine.core.models import Displayable, Ownable
from mezzanine.generic.fields import RatingField, CommentsField


class Link(Displayable, Ownable):

    link = models.URLField()
    rating = RatingField()
    score = models.IntegerField(default=0)
    comments = CommentsField()

    @models.permalink
    def get_absolute_url(self):
        return ("link_detail", (), {"slug": self.slug})


class Profile(models.Model):

    user = models.ForeignKey("auth.user")
    bio = models.TextField()
    karma = models.IntegerField(default=0, editable=False)
