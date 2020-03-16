.. _configuration:

Configuration
=============

Preparing the configuration file
--------------------------------

The default configuration file of Dru is ``dru.default.conf``. First, create a copy of this file and name it ``dru.conf``. Below the descriptions of the configuration directives are presented.

Configuration directives
------------------------

Below are the configuration directives with the possible values described. The first one or the only one is the default value.

Web server section
~~~~~~~~~~~~~~~~~~

``debug=false|true``

Puts Dru in debug mode, not suitable for regular use, when dru is in debug mode it will return debug information in case of error.

``web_host=localhost|ip_address``

Which address the web server will be bound to.

``web_enable_ssl=false|true``

Should Dru also provide TLS-secured version of the API?

``web_ssl_key_path=./web/conf/placeholder.key``

Path to the private key file used for TLS. If you do not have any certificate, we recommend obtaining one from `Let's Encrypt <https://letsencrypt.org/>`_ free certificates provider.

``web_ssl_cert_path=./web/conf/placeholder.cert``

Path to the certificate file used for TLS.

Data section
~~~~~~~~~~~~

``mongo_dir=~/dru-data/mongo``

The path for mongo database containing blocks. Space requirements for this database depends on the size of blockchain and can be quite large.

``postgres_dir=~/dru-data/pg``

The path for Postgres database containing supplementary information for Dru.

``task_results_dir=~/dru-data/task-results/``

The path for storing the tasks' results.

``zcash_dir=~/dru-data/zcash``

The path where given cryptocurrency blockchain is stored.

``rabbit_dir=~/dru-data/rabbit``

The path for RabbitMQ-related files.

Cryptocurrency node section
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For security reasons, if possible, use separate cryptocurrency client (node) for the purpose of Dru. Definitely do not use any node that has funds on its wallets.

``use_docker_zcash_node=true|false``

Should Dru use encapsulated docker node or the node installed locally?

``docker_zcash_node_test_mode=false|true``

If this option is enabled, Dru will load only 7,000 of blocks instead of the whole blockchain. Helpful for debugging.

``cryptocurrency=zcash``

Which cryptocurrency blockchain should Dru load - zcash by default, but any other cryptocurrency compliant with Bitcoin RPC should be supported.

``cryptocurrency_rpc_port=8232``

At which port the node is listening for RPC calls.

``cryptocurrency_rpc_username=user``

The RPC username to contact the node.

``cryptocurrency_rpc_password=pass``

The RPC password to contact the node.

Credentials section
~~~~~~~~~~~~~~~~~~~

``web_admin_username=admin``

The username of the web server administrator. The webserver admin portal is located at ``/admin`` URL.

``web_admin_password=pass``

The password of the web server administrator.

``mongo_admin_username=admin``

The Mongo server admin username.

``mongo_admin_password=pass``

The Mongo server admin password.

``mongo_readonly_username=user``

The Mongo server read-only username.

``mongo_readonly_password=pass``

The Mongo server read-only password.

``postgres_username=postgres``

The administrator username of the Postgres server.

``postgres_password=postgres``

The administrator password of the Postgres server.

Misc section
~~~~~~~~~~~~

``tx_address_cache_limit=1000000``

The above directive controle the cache size for tx addresses. Higher values make initial load of data faster at the cost of memory usage.

``sendgrid_username=user``

If you want to send e-mail statuses over Sendgrid, provide its username.

``sendgrid_password=changeme``

If you want to send e-mail statuses over Sendgrid, provide its password.
