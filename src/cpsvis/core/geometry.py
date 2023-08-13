
import numpy as np
from cpsvis.core.topology import TopologicalEdge, TopologicalMultiPolygon, TopologicalVertex, TopologicalPolygon, TopologicalEdgeGluing
from enum import Enum
"""
These geometric classes includes added features such as geometric gluing and geometric edge connections,
which also copy the geometric coordinates of the other geometric edge/vertex/polygon in the process.
"""

class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
class CoordinateSystem(ExtendedEnum):
    R3_COORD = 1
    CLOVERLEAF_COORD = 2

class GeometricCoordinate():
    def __init__(self):
        self.coordinates = {key: None for key in CoordinateSystem.list()}
    
    def set_coord(self, coordinate_system, coord):
        assert coordinate_system in CoordinateSystem.list(), f"Coordinate system index {coordinate_system} is not a valid coordinate system."
        self.coordinates[coordinate_system] == coord

class GeometricEdgeGluing(TopologicalEdgeGluing):
    def __init__(self, self_edge):
        super().__init__(self_edge)

class GeometricVertex(TopologicalVertex):
    """
    This defines a geometric vertex, which inherits properties from the TopologicalVertex.

    Instead of having an abstract representation such as in the TopologicalVertex, the geometric vertex is given some position x (represented as a numpy array of numbers in some coordinate system.)
    
    """
    def __init__(self, coordinate):
        super().__init__()
        self.edge_glued = GeometricEdgeGluing(self) # Uses a geometric edge gluing instead.
        assert isinstance(coordinate, GeometricCoordinate), f"Coordinate {coordinate} is not a valid GeometricCoordinate."
        self.coordinate = coordinate
    
class GeometricEdge(TopologicalEdge):
    def __init__(self, v0, v1):
        super().__init__(v0,v1)
    
    
    def add_neighbouring_edge(self, neighbour_edge, common_vertex):
        assert isinstance(neighbour_edge, GeometricEdge), f"Edge {neighbour_edge} is not a valid GeometricEdge."
        assert isinstance(common_vertex, GeometricVertex), f"Vertex {common_vertex} is not a valid GeometricVertex."
        super().add_neighbouring_edge(neighbour_edge, common_vertex)
        

