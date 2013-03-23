
Mezzit
======

Mezzit is a Reddit / Hacker News clone, built using Mezzanine.
It's intended to demonstate some of the non-CMS capabilities
of Mezzanine.

Installation
============

 $ hg clone ssh://hg@bitbucket.org/stephenmcd/mezzit
 $ cd mezzit
 $ pip install -r requirements.txt
 $ cp local_settings.py.template local_settings.py
 $ ./manage.py createdb --noinput
 $ ./manage.py runserver
