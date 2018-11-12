from igraph import Graph, STRONG


def count(db, height_from, height_to):
    blocks = get_blocks(db, height_from, height_to)
    edges = get_edges_from_blocks(blocks)
    graph = get_graph_from_edges(edges)
    v_counts = get_separate_graphs_counts(graph)
    v_counts.sort(reverse=True)
    return v_counts


def get_blocks(db, height_from, height_to):
    blocks = []
    query = db.blocks.find({'height': {'$gte': height_from, '$lte': height_to}})
    for block in query:
        blocks.append(block)
    return blocks


def get_edges_from_blocks(blocks):
    edges = []
    for block in blocks:
        for tx in block['transactions']:
            for inpt in tx['inputs']:
                for inp_addr in inpt['addresses']:
                    for outpt in tx['outputs']:
                        for out_addr in outpt['addresses']:
                            if None not in (inp_addr, out_addr):
                                edges.append((
                                    inp_addr['address'],
                                    out_addr['address'],
                                ))
    return edges


def get_graph_from_edges(edges):
    graph = Graph()
    for edge in edges:
        for vertex in edge:
            graph.add_vertex(name=vertex)
        graph.add_edge(edge[0], edge[1])
    return graph


def get_separate_graphs_counts(graph):
    v_counts = []
    for graph in graph.decompose(mode=STRONG):
        v_counts.append(graph.vcount())
    return v_counts
