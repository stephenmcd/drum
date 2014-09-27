from __future__ import unicode_literals

from . import poll_rss


class Command(poll_rss.Command):

    def link_from_entry(self, entry):
        """
        For link posts on Tumblr, the real URL is contained
        in the HTML summary.
        """
        return entry.summary.split('href="')[1].split('"')[0]
