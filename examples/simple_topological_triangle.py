
from cpsvis.core.topology import TopologicalEdge, TopologicalVertex, TopologicalTriangle

# v11 = TopologicalVertex()
# v12 = TopologicalVertex()
# edge1 = TopologicalEdge(v11, v12)

# v21 = TopologicalVertex()
# v22 = TopologicalVertex()
# edge2 = TopologicalEdge(v21, v22)

# edge1.edge_glued.glue_edge(edge2, v21, v22)


triangle = TopologicalTriangle()


v0 = TopologicalVertex()
v1 = TopologicalVertex()
v2 = TopologicalVertex()

e1 = TopologicalEdge(v0,v1)
e2 = TopologicalEdge(v1, v2)
e3 = TopologicalEdge(v2, v0)

triangle.add_disjoint_edge(e1)
triangle.add_vertex_connected_edge(e1, e2, v1)
triangle.add_vertex_connected_edge(e2, e3, v2)
e3.add_neighbouring_edge(e1, v0)

triangle.check_closed()

# print(triangle.edges[0].neighbouring_edges)
# edge = triangle.edges[0]
# assert isinstance(edge, TopologicalEdge)
