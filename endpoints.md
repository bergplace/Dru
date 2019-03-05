The list of endpoints provided by Dru.

The most basic endpoint is returning the blocks given the following criteria:

Endpoints - blocks:

	get_blocks_range(start_height, end_height)
    	Returns the blocks from start_height to end_height.

    	Requires:
			start_height >= 0
			end_height >= start_height
       		end_height, start_height <= max_height

       If the requirements are not met, the endpoint returns an error.

	get_blocks_range(start_height, num_of_blocks)
		Returns the num_of_blocks blocks from start_height. This endpoint can
		return blocks from start_height in both directions, i.e., lower than
		and higher than start_height (including start_height).

		Requires:
			num_of_blocks != 0
			start_height >= 0
			start_height + num_of_blocks >= 0
			start_height + num_of_blocks <= max_height

Next level of abstraction is the list of nodes and edges as a future foundation of a graph
for further processing.

Assumptions:
	- the basic entity understood as a node is an address
	- the link is represented by the transaction
	- since there are multiple inputs and outputs possible, the only possiblity to link nodes
  	  in the transaction ID, thus it will be the link attribute within all the resulting source rows
	- the decision of the researcher is how to deal with it in terms of further building the graph
	- however, the endpoints calculating graph metrics and measures will have parameters controllable
  	  by the user on how to build the graph before computing anything further
	- the link can be accompanied by some more attributes, but for limiting the data transfer, it is
  	  advised to use getTXAttributes endpoint in order to obtain the all or attributes of the transaction

Endpoints - edges:

	getEdges(startBlockID, endBlockID, [attributes])
		Returns the list of edges starting from startBlockID build from numOfBlocks blocks.

	getEdges(startBlockID, numOfBlocks, [attributes])
		Returns the list of edges starting from block startBlockID to endBlockID.

	The [attributes] are the optional attributes that will be added to the list of edges.

	getTransactionAttrs(transactionID, [attributes])
		Returns all/selected attributes of a transaction provided by transactionID.

The next set of endpoints is the core of Dru, since the above ones are rather for self-programmed experiments
if any andpoint listed below does not apply to the experimental scenario.

Endpoints - network science: