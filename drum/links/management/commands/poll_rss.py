from __future__ import unicode_literals

from datetime import datetime
from time import mktime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import get_default_timezone, make_aware
from feedparser import parse
import requests

from mezzanine.generic.models import Rating

from drum.links.models import Link


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("urls", nargs="*")
        parser.add_argument(
            "--follow",
            action="store_true",
            dest="follow",
            default=False,
            help="Make a HTTP request for every link imported and follow "
                 "redirects, storing the final URL."
        )
        parser.add_argument(
            "--follow-old",
            action="store_true",
            dest="follow_old",
            default=False,
            help="Will go back and run --follow aginst previously added links"
        )

    def handle(self, **options):
        if options["follow_old"]:
            self.follow_old()
            return
        try:
            user_id = User.objects.filter(is_superuser=1)[0].id
        except IndexError:
            return
        for url in options["urls"]:
            for entry in parse(url).entries:
                link = self.entry_to_link_dict(entry)
                if options["follow"]:
                    try:
                        link["link"] = self.follow_redirects(link["link"])
                    except Exception as e:
                        print "%s - skipping %s" % (e, link["link"])
                        continue
                link["user_id"] = user_id
                try:
                    obj = Link.objects.get(link=link["link"])
                except Link.DoesNotExist:
                    obj = Link.objects.create(**link)
                    obj.rating.add(Rating(value=1, user_id=user_id),
                        bulk=False)
                    print "Added %s" % obj

    def link_from_entry(self, entry):
        """
        Subclasses can override this to perform custom link
        extraction from an entry - eg Tumblr link posts
        will contain the real link inside the summary.
        """
        return entry.link

    def entry_to_link_dict(self, entry):
        link = {
            "title": entry.title,
            "link": self.link_from_entry(entry),
            "gen_description": False,
        }
        try:
            publish_date = entry.published_parsed
        except AttributeError:
            pass
        else:
            publish_date = datetime.fromtimestamp(mktime(publish_date))
            publish_date = make_aware(publish_date, get_default_timezone())
            link["publish_date"] = publish_date
        return link

    def follow_redirects(self, link):
        final = requests.get(link).url
        print "followed %s to %s" % (link, final)
        return final

    def follow_old(self):
        for link in Link.objects.all():
            try:
                new_url = self.follow_redirects(link.link)
            except Exception as e:
                print "%s - skipping %s" % (e, link.link)
            else:
                Link.objects.filter(id=link.id).update(link=new_url)
