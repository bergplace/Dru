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

Dru runs in the Docker environment. Before continuing with installing Dru, please make sure that you have Docker CE and Docker Compose installed. The following guide shows how to install Docker CE: https://docs.docker.com/install/ and this one describes the installation process of Docker Compose: https://docs.docker.com/compose/install/

Cloning the repository
~~~~~~~~~~~~~~~~~~~~~~

If you have Docker CE installed, you can proceed to cloning the Dru repository::

    git clone https://github.com/bergplace/Dru.git

Note, that the Docker compose file provided by Dru has version 3.3 and as such it requires Docker in version 17.06.0 or above. For more details on compatibility, please visit this webpage: https://docs.docker.com/v17.09/compose/compose-file/

Creating the configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, use the default configuration file as a template for your Dru instance configuration::

    cd Dru
    cp dru.conf.default dru.conf

Then, edit the dru.conf to suite your needs according to the :ref:`configuration` section.

Starting Dru
------------

When you prepared the configuration file, you are ready to start Dru. But before have a look also at all make targets by issuing the following command::

    make help

Most likely, you will want to start Dru in the following manner::

    make start

It is worth to know that Dru also offers the ``make target`` directive that loads only first 7,000 of blocks and lets to test the whole environment without downloading the whole blockchain. All make targets are described in the :ref:`maketargets` section.

Using Dru
---------

When Dru runs for the first time, it imports all blockchain blocks information into its MongoDB instance. This will take some time and you can see the progress using the following make target::

    make logs

Nevertheless, as soon as some blocks are in MongoDB, you can communicate with the endpoints.

Assuming that the Dru instance is installed on your localhost, you can try to test the environment by querying the API for a block. To do so, use your REST client (e.g. web browser) and make the following query::

    http://localhost:8000/api/get_blocks/0/0

This call will return a JSON object that contains the URL to the actual result (result_url). If you follow this URL, you will get another JSON that contains the status of the query in the field "status". If the results are already available, they will be in the "data" field.

If you are running Dru for Zcash, this call return the Zcash genesis block.

If everything worked well, you can continue using Dru. For the documentation of all Dru API endpoints, see :ref:`api` section. Otherwise, if you'll encounter any problems, please have a look at Dru logs by running the command ``make logs``. If you won't find anything helpful, try to look for support using the :ref:`support` section.

Stopping Dru
------------

When you wish to stop Dru instance, issue the following command::

    make stop