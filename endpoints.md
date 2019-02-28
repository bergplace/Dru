The list of endpoints provided by Dru.

The most basic endpoint is returning the blocks given the following criteria:

Endpoints - blocks:

	getBlocks(startBlockID, endBlockID)
    	Returns the blocks from startBlockID to endBlockID.

    	Requires:
			startBlockID >= 0
			endBlockID >= startBlockID
       		endBlockID, startBlockID <= maxBlockID

       If the requirements are not met, the endpoint returns an error.

	getBlocks(startBlockID, numOfBlocks)
		Returns the numOfBloks blocks from startBlockID. This endpoint can
		return blocks from startBlockID in both directions, i.e., lower than
		and higher than startBlockID (including startBlockID).

		Requires:
			numOfBloks != 0
			startBlockID + numOfBlocks >= 0
			startBlockID + numOfBlocks <= maxBlockID

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