
import numpy as np
from cpsvis.core.topology import TopologicalEdge, TopologicalMultiPolygon, TopologicalVertex, TopologicalPolygon, TopologicalEdgeGluing

"""
These geometric classes includes added features such as geometric gluing and geometric edge connections,
which also copy the geometric coordinates of the other geometric edge/vertex/polygon in the process.
"""

class GeometricEdgeGluing(TopologicalEdgeGluing):
    def __init__(self):
        super().__init__()

class GeometricVertex(TopologicalVertex):
    """
    This defines a geometric vertex, which inherits properties from the TopologicalVertex.

    Instead of having an abstract representation such as in the TopologicalVertex, the geometric vertex is given some position x (represented as a numpy array of numbers in some coordinate system.)
    
    """
    def __init__(self):
        super().__init__()
        self.edge_glued = GeometricEdgeGluing(self) # Uses a geometric edge gluing instead.
        
