.. _maketargets:

Make targets
============

These are the most general make targets. In order to see all of them, please refer to the content of the Makefile.

``make help``

Shows the help message.

``make restart``

Restarts Dru.

``make start``

Starts Dru in the regular production mode using ``dru.default.conf`` as the initial configuration file. Before starting, verify configuration settings in this file.

``make test``

Starts Dru in the testing mode. This includes running the Travis tests as well as importing only first 7000 blocks. For details on the test configuration, please see ``dru.test.conf``.

``make fuzz``

Starts the "fuzz" tests, calling multiple Dru endpoints with variety of parameters. This allows to verify whether Dru's endpoints are working properly. Before starting, please update the ``URL`` directive in ``test/fuzz.py``.

``make html``

Generates the webpages (index, mail registration etc.).

In order to see some more detailed targets that build the ones described above, have a look at ``Makefile`` content itself.