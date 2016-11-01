
Drum
====

Created by `Stephen McDonald <http://twitter.com/stephen_mcd>`_

Drum is a Reddit / Hacker News clone, built using `Mezzanine`_
and `Django`_. It is `BSD licensed`_, and designed to demonstrate
some of the non-CMS capabilities of Mezzanine, such as threaded
comments, ratings, and public user accounts.

Check out the blog post `Building Social Apps with Mezzanine`_,
which contains a detailed walk-through of how Drum was built. A
`live demo of Drum`_ is also available.

Dependencies
============

Drum is designed as a plugin for the `Mezzanine`_ content management
platform, and therefore requires `Mezzanine`_ to be installed. The
integration of the two applications should occur automatically by
following the installation instructions below.

Installation
============

The easiest method is to install directly from PyPI using `pip`_ by
running the command below, which will also install the required
dependencies mentioned above::

    $ pip install -U drum

Otherwise, you can download Drum and install it directly from source::

    $ python setup.py install

Once installed, the command ``mezzanine-project`` can be used to
create a new Mezzanine project, with Drum installed, in similar
fashion to ``django-admin.py``::

    # FIXME: add new instructions of how to create a project with drum
    $ mezzanine-project -a drum project_name
    $ cd project_name
    $ python manage.py createdb --noinput
    $ python manage.py runserver

Here we specify the ``-a`` switch for the ``mezzanine-project`` command,
which tells it to use an alternative package (drum) for the project
template to use. Both Mezzanine and Drum contain a project template
package containing the ``settings.py`` and ``urls.py`` modules for an
initial project. If you'd like to add Drum to an existing Mezzanine
or Django project, you'll need to manually configure these yourself. See
the `FAQ section of the Mezzanine documentation`_ for more information.

.. note::

    The ``createdb`` is a shortcut for using Django's ``syncdb``
    command and setting the initial migration state. You
    can alternatively use ``syncdb`` and ``migrate`` if preferred.

You should then be able to browse to http://127.0.0.1:8000/admin/ and
log in using the default account (``username: admin, password:
default``). If you'd like to specify a different username and password
during set up, simply exclude the ``--noinput`` option included above
when running ``createdb``.

RSS Import
==========

One difficulty faced with a Drum site is building up an initial user
base, as well as a good amount of interesting link content. This is
a bit of a chicken and egg problem, in that each of these depends on
the other. One way to address this is to automatically populate
the site with interesting links. To help with this, Drum provides the
Django management command ``poll_rss`` for retrieving links from an RSS
feed, and populating the site with them. For example, suppose I was a
terrible person and wanted to populate my Drum site with links directly
from the Hacker News front page and the programming section of Reddit::

    python manage.py poll_rss https://news.ycombinator.com/rss http://www.reddit.com/r/programming/.rss

Here you can see multiple RSS feeds being passed to the command, which
I could then run on a scheduled basis using a cron job. Note that to
use the ``poll_rss`` command, you'll need the `feedparser`_ library
installed.

Auto Tagging
============

Drum provides some basic support for automatically tagging new links
as they're added. This is first configured by setting the ``AUTO_TAG``
setting to ``True``. With that set, when a new link is added, its
given title is broken up into keywords, and if those keywords already
exist as tags in the database, they're applied to the newly added link.

This means that for auto-tagging to work, the tags must already exist
in the database. You can either add them manually via the admin (under
the "Keywords" section), or if you have a large number of existing
links, you can use the ``auto_tag`` management command Drum provides,
which will analyse the titles of all your existing links, and provide
tags it extracts from them. This makes use of the `topia.termextract`_
package which you'll first need to install::

    python manage.py auto_tag --generate=100 --assign --remove

The ``--generate`` option must be provided to extract tags, and limits
the number of tags extracted. Generally more tags will be extracted
than are relevant, depending on your existing set of links, so
experiment with different values here. You'll likely want to review all
the tags added, deleting some and manually editing others, via the
Django admin interface. The ``--assign`` option will go back and assign
all tags in the database to all links in the database, as would occur
if they were newly created. The ``--remove`` option will cause all
existing tags to be removed.

You can also define your own tag extraction function, if splitting the
title on spaces doesn't suffice. To do so, define the setting
``AUTO_TAG_FUNCTION`` which should contain a string with the Python
dotted path to your custom tag function. The function will be given an
unsaved ``Link`` object, and should return a sequence of tags to add.


Contributing
============

Drum is an open source project managed using both the Git and
Mercurial version control systems. These repositories are hosted on
both `GitHub`_ and `Bitbucket`_ respectively, so contributing is as
easy as forking the project on either of these sites and committing
back your enhancements.

Please note the following guidelines for contributing:

  * Contributed code must be written in the existing style. This is
    as simple as following the `Django coding style`_ and (most
    importantly) `PEP 8`_.
  * Contributions must be available on a separately named branch
    based on the latest version of the main branch.
  * Run the tests before committing your changes. If your changes
    cause the tests to break, they won't be accepted.
  * If you are adding new functionality, you must include basic tests
    and documentation.

Donating
========

If you would like to make a donation to continue development of
Drum, you can do so via the `Mezzanine Project`_ website.

Support
=======

To report a security issue, please send an email privately to
`security@jupo.org`_. This gives us a chance to fix the issue and
create an official release prior to the issue being made
public.

For general questions or comments, please join the `mezzanine-users`_
mailing list. To report a bug or other type of issue, please use the
`GitHub issue tracker`_. And feel free to drop by the `#mezzanine
IRC channel`_ on `Freenode`_, for a chat.

Sites Using Drum
================

* `Food News <http://food.hypertexthero.com>`_

.. _`Building Social Apps with Mezzanine`: http://blog.jupo.org/2013/04/30/building-social-apps-with-mezzanine-drum/
.. _`Django`: http://djangoproject.com/
.. _`BSD licensed`: http://www.linfo.org/bsdlicense.html
.. _`live demo of Drum`: http://drum.jupo.org/
.. _`Mezzanine`: http://mezzanine.jupo.org/
.. _`Mezzanine Project`: http://mezzanine.jupo.org/
.. _`pip`: http://www.pip-installer.org/
.. _`FAQ section of the Mezzanine documentation`: http://mezzanine.jupo.org/docs/frequently-asked-questions.html#how-can-i-add-mezzanine-to-an-existing-django-project
.. _`Django coding style`: http://docs.djangoproject.com/en/dev/internals/contributing/#coding-style
.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/
.. _`feedparser`: http://code.google.com/p/feedparser/
.. _`topia.termextract`: https://pypi.python.org/pypi/topia.termextract/
.. _`Github`: http://github.com/stephenmcd/drum/
.. _`Bitbucket`: http://bitbucket.org/stephenmcd/drum/
.. _`Github issue tracker`: http://github.com/stephenmcd/drum/issues
.. _`security@jupo.org`: mailto:security@jupo.org?subject=Mezzanine+Security+Issue
.. _`mezzanine-users`: http://groups.google.com/group/mezzanine-users
.. _`#mezzanine IRC channel`: irc://freenode.net/mezzanine
.. _`Freenode`: http://freenode.net
