.. _changelog:

Changelog
=========

Unreleased
----------

Added:

- wait-for-it.sh script to celery & web containers for waiting for postgres to start

Changed:

- update python-igraph to version 0.8.0

- update psycopg2 to psycopg2-binary and bump from 2.7.7 to 2.8.4

- update fuzz test URL to localhost to not to hit the demo instance

- reduce fuzz test intensity

Fixed:

- fix endpoints computing transivitity, now they work only with simplified undirected graphs

1.0.0 - 2019-08-19
------------------

First public release.
