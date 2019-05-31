.. _getting-started:

Getting started
===============

Where to install Dru?
---------------------

Dru can be thought as of an engine that provides its clients with answers on blockchain-related queries. As such, it can be run on your local computer, but bear in mind that if the blockchain of a chosen cryptocurrency is large, you need to be equipped with enough hardware (especially RAM). Apart from that, some of the queries can be computationally complex, so this is another factor to consider. This is why it is suggested to have Dru installed on either a server or a workstation that is always on and has enough resources. This will create a typical client-server architecture and many researchers will have the opportunity to use Dru at the same time and gain access to already computed queries' results. Nevertheless, this is not a necessity and you can install Dru on your local computer.


Installing Dru
--------------

Installing docker
~~~~~~~~~~~~~~~~~

Dru runs in the Docker environment. Before continuing with installing Dru, please make sure that you have Docker CE installed. The following guide shows how to install Docker CE: https://docs.docker.com/install/


Cloning the repository
~~~~~~~~~~~~~~~~~~~~~~

If you have Docker CE installed, you can proceed to cloning the Dru repository::

    git clone https://github.com/bergplace/Dru.git

Creating the configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, use the default configuration file as a template for your Dru instance configuration::

    cd Dru
    cp dru.conf.default dru.conf

Please do edit the dru.conf to suite your needs according to the :ref:`configuration` section.

Starting Dru
~~~~~~~~~~~~

When you prepared the configuration file, you are ready to start Dru. But before please have a look also at all make options by issuing the following command::

    make help

Most likely, you will want to start Dru in the following manner::

    make start


Stopping Dru
~~~~~~~~~~~~

When you wish to stop Dru instance, issue the following command::

    make stop