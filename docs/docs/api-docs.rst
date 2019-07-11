.. _api:

API endpoints
=============

.. code:: python

    def get_blocks(start_height, end_height)

Returns the list of blocks for a given range of blocks' heights.
The returned JSON can be used for further processing if none of the endpoints
is suitable for performing the requested analysis.
Note that this endpoint returns whole blocks, no attributes are stripped.

.. code:: python

    def get_blocks_reduced(start_height, end_height)

Returns the list of blocks for a given range of blocks' heights, yet with limited fields.

The returned fields are the following:

* height

* time

* transaction id

* input addresses (or coinbase)

* output addresses

* value
 
As such, this is a limited version of ``get_blocks`` endpoint.

The returned JSON can be used for further processing if none of the endpoints is suitable for performing the requested analysis.

.. code:: python

    def get_edges(start_height, end_height)

Returns the list of edges blocks for a given range of blocks' heights. These edges can be easily imported into graph-processing libraries.

Fields returned:

* source address

* destination address

* value of the transactions

* block height

* block time

.. code:: python

    def get_degree(start_height, end_height, mode)

Returns the list of addresses and the value of degree corresponding to them.

The graph is created from the blocks in the range [start_height, end_height].

The graph will be built as directed, but using mode all variants of the measure can be computed:

* all - total degree of the node

* in - in-degree of the node

* out - out-degree

.. code:: python

    def get_degree_by_block(start_height, end_height, address, mode)

Returns the list of addresses and the value of degree corresponding to them.
The graph is created from the blocks in the range [start_height, end_height].
This variant computes the degree in each block separately.
The graph will be built as directed, but using mode all variants of the measure can be computed:

* all - total degree of the node

* in - in-degree of the node

* out - out-degree

.. code:: python

    def get_degree_max(start_height, end_height, mode)

Returns the list of addresses and the value of degree corresponding to them.
The graph is created from the blocks in the range [start_height, end_height].
The graph will be built as directed, but using mode all variants of the measure can be computed:

* all - total degree of the node

* in - in-degree of the node

* out - out-degree

.. code:: python

    def get_betweenness(start_height, end_height, directed)

Returns the list of addresses and the value of betweenness corresponding to them.
The graph is created from the blocks in the range [start_height, end_height].
The graph can be built either as directed or undirected.
Note: as all shortest paths have to be computed, this operation is time-consuming. Use with care.


.. code:: python

    def get_betweenness_max(start_height, end_height, directed)

Returns the address and the value of betwenneess in the graph created
The graph is created from the from the blocks in the range [start_height, end_height].
The graph can be built either as directed or undirected.
Note: as all shortest paths have to be computed, this operation is time-consuming. Use with care.

.. code:: python

    def get_closeness(start_height, end_height, directed)

Returns the list of addresses and the value of closeness corresponding to them.
The graph is created from the from the blocks in the range [start_height, end_height].
The graph can be built either as directed or undirected.

.. code:: python

    def get_closeness_max(start_height, end_height, directed)

Returns the address and the value of the closeness in the graph.
The graph is created from the from the blocks in the range [start_height, end_height].
The graph can be built either as directed or undirected.

.. code:: python

    def get_transitivity(start_height, end_height)

Returns the nodes' clustering coefficient in the graph.
The graph is created from the blocks in the range [start_height, end_height]
For global clustering coefficient value, use for get_transitivity_global.

.. code:: python

    def get_transitivity_global(start_height, end_height)

Returns the clustering coefficient of the graph created from the blocks in the range [start_height, end_height].
This value is global for the graph. For node-level clustering coefficient, use get_transitivity.

.. code:: python

    def get_diameter(start_height, end_height, directed)

Returns the diameter of the graph created from the blocks in the range [start_height, end_height].
The graph can be considered as directed or undirected.

.. code:: python

    def get_density(start_height, end_height, directed, loops)

Returns the density of the graph created from the blocks in the range [start_height, end_height].
The graph can be considered as directed or undirected.

.. code:: python

    def are_connected(start_height, end_height, address1, address2, directed)

Returns true/false information whether two addresses are connected within a given range of blocks.
If any of these addresses does not exist in the graph, None will be returned.

.. code:: python

    def get_transactions_value(start_height, end_height, address1, address2)

Returns the count and total value of transactions between two addresses in the graph.
The graph is created from the blocks in the range [start_height, end_height].
If any of these addresses does not exist in the graph, None will be returned.
