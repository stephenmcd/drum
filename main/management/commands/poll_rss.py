
from datetime import datetime
from time import mktime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import get_default_timezone, make_aware
from feedparser import parse

from mezzanine.generic.models import Rating

from ...models import Link


class Command(BaseCommand):

    def handle(self, *urls, **options):
        try:
            user_id = User.objects.filter(is_superuser=1)[0].id
        except IndexError:
            return
        for url in urls:
            for entry in parse(url).entries:
                link = self.entry_to_link_dict(entry)
                link["user_id"] = user_id
                try:
                    obj = Link.objects.get(link=link["link"])
                except Link.DoesNotExist:
                    obj = Link.objects.create(**link)
                    obj.rating.add(Rating(value=1, user_id=user_id))

    def entry_to_link_dict(self, entry):
        link = {"title": entry.title, "gen_description": False}
        try:
            link["link"] = entry.summary.split('href="')[2].split('"')[0]
        except IndexError:
            link["link"] = entry.link
        try:
            publish_date = entry.published_parsed
        except AttributeError:
            pass
        else:
            publish_date = datetime.fromtimestamp(mktime(publish_date))
            publish_date = make_aware(publish_date, get_default_timezone())
            link["publish_date"] = publish_date
        return link
