
from time import time

from django.conf import settings
from django.db import models
from mezzanine.core.models import Displayable, Ownable
from mezzanine.core.managers import DisplayableManager
from mezzanine.generic.fields import RatingField, CommentsField


class LinkManager(DisplayableManager):

    def by_score(self):
        gravity = 2
        queryset = self.select_related("user")
        seconds = time()
        engine = settings.DATABASES[self.db]["ENGINE"].rsplit(".", 1)[1]
        if engine in ("postgresql_psycopg2", "mysql"):
            score = "rating_sum / POW(seconds - %s, %s)" % (seconds, gravity)
            extra = {"select": {"score": score}}
            return queryset.extra(**extra).order_by("-score")
        else:
            for obj in queryset:
                score = obj.rating_sum / pow(obj.seconds - seconds, gravity)
                setattr(obj, "score", score)
            return sorted(queryset, key=lambda obj: obj.score, reverse=True)


class Link(Displayable, Ownable):

    link = models.URLField()
    rating = RatingField()
    seconds = models.FloatField(default=time)
    comments = CommentsField()

    objects = LinkManager()

    @models.permalink
    def get_absolute_url(self):
        return ("link_detail", (), {"slug": self.slug})


class Profile(models.Model):

    user = models.ForeignKey("auth.user")
    bio = models.TextField()
    karma = models.IntegerField(default=0, editable=False)
