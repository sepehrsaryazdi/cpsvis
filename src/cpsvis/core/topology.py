import numpy as np


class TopologicalVertex:
    def __init__(self, uid=0):
        self.neighbouring_vertices = []
        self.uid = uid
        self.parent_edges = []

    def set_uid(self,uid):
        self.uid = uid
    
    def add_parent_edge(self, edge):
        assert isinstance(edge, TopologicalEdge), f"Edge {edge} is not a valid TopologicalEdge."
        self.parent_edges.append(edge)
    


class TopologicalEdge:
    def __init__(self, v0, v1, uid=0):
        assert isinstance(v0, TopologicalVertex), f"Vertex {v0} is not a valid TopologicalVertex."
        assert isinstance(v1, TopologicalVertex), f"Vertex {v1} is not a valid TopologicalVertex."
        self.v0 = v0
        self.v1 = v1
        assert v0 != v1, "Can't assign the same vertex to the endpoints of edge."
        self.vertices = [v0,v1]
        self.uid = uid
        self.parent_polyons = []
    
    def add_parent_polygon(self, polygon):
        assert isinstance(polygon, TopologicalPolygon), f"Polygon {polygon} is not a valid TopologicalPolygon."
        self.parent_polyons.append(polygon)
    
    def set_uid(self, uid):
        self.uid = uid
    
    def set_children_uid(self, uid1, uid2):
        self.v0.set_uid(uid1)
        self.v0.set_uid(uid2)
    
    def add_children_edge_self(self):
        self.v0.add_parent_edge(self)
        self.v1.add_parent_edge(self)

class TopologicalPolygon:
    def __init__(self, uid=0):
        self.vertices = []
        self.edges = []
        self.uid = uid
    
    def add_disjoint_edge(self, edge):
        assert isinstance(edge, TopologicalEdge), f"Edge {edge} is not a valid TopologicalEdge."
        self.edges.append(edge)
    
    # def add_edge_intersecting_vertex(self, edge_on_self, new_edge, intersecting_vertex):
    #     assert isinstance(edge_on_self, TopologicalEdge), f"Edge {edge_on_self} is not a valid TopologicalEdge."
    #     assert isinstance(new_edge, TopologicalEdge), f"Edge {new_edge} is not a valid TopologicalEdge."
    #     assert isinstance(intersecting_vertex, TopologicalVertex), f"Vertex {intersecting_vertex} is not a valid TopologicalVertex."
        
    #     assert self in edge_on_self.parent_polyons, f"Edge on parentself does not have a parent polygon as self."
    #     assert (intersecting_vertex in edge_on_self.vertices) and (intersecting_vertex in new_edge.vertices), f"Interescting vertex is not a valid intersection of the edges."



    def set_uid(self, uid):
        self.uid = uid
    
    def add_children_polygon_self(self):
        for edge in self.edges:
            assert isinstance(edge, TopologicalEdge), f"Edge {edge} is not a valid TopologicalEdge."
            edge.add_parent_polygon(self)
    
    def set_edge_children_uid(self, uid_list):
        assert len(uid_list) == len(self.edges)
        for edge, i in enumerate(self.edges):
            assert isinstance(edge, TopologicalEdge), f"Edge {edge} is not a valid TopologicalEdge."
            uid = uid_list[i]
            edge.set_uid(uid)
    
    def set_vertex_children_uid(self, uid_list):
        assert len(uid_list) == len(self.vertices)
        for vertex, i in enumerate(self.vertices):
            assert isinstance(vertex, TopologicalEdge), f"Vertex {vertex} is not a valid TopologicalVertex."
            uid = uid_list[i]
            vertex.set_uid(uid)
    
    def initialise_edge(self):
        v0 = TopologicalVertex(0)
        v1 = TopologicalVertex(1)
        edge = TopologicalEdge(v0,v1)
        edge.add_children_edge_self()
        edge.add_parent_polygon(self)
        self.add_disjoint_edge(edge)

class TopologicalMultiPolygon:
    def __init__(self, uid=0):
        self.polygons = []
        self.uid = uid
    
    def set_uid(self, uid):
        self.uid = uid
    
    def set_polygon_children_uid(self, uid_list):
        assert len(uid_list) == len(self.polygons)
        for polygon, i in enumerate(self.polygons):
            assert isinstance(polygon, TopologicalPolygon), f"Polygon {polygon} is not a valid TopologicalPolygon."
            uid = uid_list[i]
            polygon.set_uid(uid)
            
    
    
