
from datetime import datetime
from time import mktime

from django.core.management.base import BaseCommand
from django.utils.timezone import get_default_timezone, make_aware
from feedparser import parse

from ...models import Link


class Command(BaseCommand):

    def handle(self, *urls, **options):
        for url in urls:
            for entry in parse(url).entries:
                link = self.entry_to_link_dict(entry)
                try:
                    Link.objects.get(link=link["link"])
                except Link.DoesNotExist:
                    Link.objects.create(**link)

    def entry_to_link_dict(self, entry):
        link = {"title": entry.title, "user_id": 1, "gen_description": False}
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
