
Created by `Stephen McDonald <http://twitter.com/stephen_mcd>`_

Drum
====

Drum is a Reddit / Hacker News clone, built using Mezzanine.
It is intended to demonstate some of the non-CMS capabilities
of Mezzanine, such as threaded comments, ratings, and public
user accounts.

Check out the blog post `Building Social Apps with Mezzanine
<http://blog.jupo.org/2013/04/30/building-social-apps-with-mezzanine-drum/>`_,
which contains a detailed walk-through of how Drum was built.

Installation
============

Basic setup::

  $ hg clone ssh://hg@bitbucket.org/stephenmcd/drum
  $ cd drum
  $ pip install -r requirements.txt
  $ cp local_settings.py.template local_settings.py
  $ ./manage.py createdb --noinput
  $ ./manage.py runserver

Sites Using Drum
================

* `Food News <http://food.hypertexthero.com>`_


