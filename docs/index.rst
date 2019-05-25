.. _index:

.. Dru documentation master file, created by
   sphinx-quickstart on Tue Mar  5 16:53:45 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

About Dru
=========

What is Dru?
------------

Dru is a platform that enables the researchers focused on the analysis of blockchain an easier start. It consists from a block engine that maintains the blocks database in sync with the blockchain of a cryptocurrency and a querying engine that offers its API to run the analyses. The results of each query are stored and are easily accessible for reducing time of reproducing them.

Which blockchains are currently supported by Dru?
-------------------------------------------------

Dru is designed in such a way that each blockchain client using standard RPC calls should be supported. Nevertheless, the development and testing focused especially on `Zcash <https://z.cash/>`_, since the development process was supported by the `Zcash Foundation <https://www.zfnd.org/>`_. For details see :ref:`funding`.

Where would I find the sources of Dru?
--------------------------------------

Dru is an open source project and can be found here: https://github.com/bergplace/Dru. The lincense details are to be found in :ref:`license` page.

OK, I'm am insterested in using Dru, what's next?
-------------------------------------------------

Great! Please have a look at the :ref:`getting-started` guide.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   docs/getting-started
   docs/configuration
   docs/api-docs
   docs/server
   docs/version-history
   docs/source-code
   docs/authors
   docs/funding
   docs/license
   docs/contact
