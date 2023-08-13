
from cpsvis.core.topology import TopologicalEdge, TopologicalVertex

v11 = TopologicalVertex()
v12 = TopologicalVertex()
edge1 = TopologicalEdge(v11, v12)

v21 = TopologicalVertex()
v22 = TopologicalVertex()
edge2 = TopologicalEdge(v21, v22)

edge1.edge_glued.glue_edge(edge2, v21, v22)