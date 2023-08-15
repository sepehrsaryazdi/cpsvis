
from cpsvis.core.topology import TopologicalEdge, TopologicalVertex, TopologicalPolygon

polygon = TopologicalPolygon()


v0 = TopologicalVertex()
v1 = TopologicalVertex()
v2 = TopologicalVertex()
v3 = TopologicalVertex()

e1 = TopologicalEdge(v0,v1)
e2 = TopologicalEdge(v1, v2)
e3 = TopologicalEdge(v2, v3)
e4 = TopologicalEdge(v3, v0)

polygon.add_disjoint_edge(e1)
polygon.add_vertex_connected_edge(e1, e2, v1)
polygon.add_vertex_connected_edge(e2, e3, v2)
polygon.add_vertex_connected_edge(e3, e4, v3)
e4.add_neighbouring_edge(e1, v0)

polygon.auto_index_children()

print(polygon.index_to_vertex_hash)
print(polygon.edge_index_increasing_hash())

# print(polygon.check_closed())

