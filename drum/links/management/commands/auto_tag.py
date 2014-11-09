from __future__ import unicode_literals

from optparse import make_option
from string import punctuation

from django.db import connection
from django.core.management.base import BaseCommand
from mezzanine.generic.models import AssignedKeyword, Keyword
from mezzanine.utils.urls import slugify

from drum.links.models import Link


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option("--generate", dest="generate", type=int),
        make_option("--remove", dest="remove", action="store_true",
            default=False),
        make_option("--assign", dest="assign", action="store_true",
            default=False),
    )

    def handle(self, *urls, **options):
        cursor = connection.cursor()
        if options["remove"]:
            cursor.execute("DELETE FROM generic_assignedkeyword;")
            cursor.execute("DELETE FROM generic_keyword;")
        if options["generate"]:
            self.generate(options["generate"])
        if options["assign"]:
            cursor.execute("DELETE FROM generic_assignedkeyword;")
            Link.objects.update(keywords_string="")
            for link in Link.objects.all():
                print("Assigning to %s" % link)
                link.save()

    def generate(self, size):

        try:
            from topia.termextract import extract
        except ImportError:
            print("topia.termextract library required")
            return

        extractor = extract.TermExtractor()
        extractor.filter = extract.permissiveFilter
        titles = Link.objects.values_list("title", flat=True)
        tags = extractor(" ".join(titles))
        tags.sort(key=lambda tag: tag[1], reverse=True)

        def valid_tag(tag):
            def valid_char(char):
                return not (char in punctuation or char.isdigit())
            return filter(valid_char, slugify(tag[0]))

        for tag in filter(valid_tag, tags)[:size]:
            print("Creating keyword %s" % tag[0])
            Keyword.objects.get_or_create(title=tag[0])
