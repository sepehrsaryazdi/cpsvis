import numpy as np

class EdgeGluing:
    """
    Class which is instantiated within every TopologicalEdge to keep track of what edge this particular edge is glued to, if any.
    """
    def __init__(self, self_edge):
        self.self_edge = self_edge
        self.edge_glued = None
        self.edge_glued_first_vertex = None
        self.edge_glued_second_vertex = None
    
    def glue_edge(self, edge_to_glue, first_vertex, second_vertex):
        """
        Glues this edge to edge_to_glue with orientation defined as this edge's first vertex being glued to the first_vertex of the edge_to_glue, and the second vertex being glued to second_vertex.
        This function will also update the other edge's knowledge of which edge it is glued to, that is, it will be glued to this edge.
        Example 1:
        v11 = TopologicalVertex()
        v12 = TopologicalVertex()
        edge1 = TopologicalEdge(v11, v12)

        v21 = TopologicalVertex()
        v22 = TopologicalVertex()
        edge2 = TopologicalEdge(v21, v22)

        edge1.edge_glued.glue_edge(edge2, v21, v22)

        This corresponds to edge1 and edge2 being identified with the same orientation.

        Example 2:
        v11 = TopologicalVertex()
        v12 = TopologicalVertex()
        edge1 = TopologicalEdge(v11, v12)

        v21 = TopologicalVertex()
        v22 = TopologicalVertex()
        edge2 = TopologicalEdge(v21, v22)

        edge1.edge_glued.glue_edge(edge2, v22, v21)

        This corresponds to edge1 and edge2 being identified with opposite orientations.
        """
        assert isinstance(edge_to_glue, TopologicalEdge), f"Edge {edge_to_glue} is not a valid TopologicalEdge."
        assert isinstance(first_vertex, TopologicalVertex), f"Vertex {first_vertex} is not a valid TopologicalVertex."
        assert isinstance(second_vertex, TopologicalVertex), f"Vertex {second_vertex} is not a valid TopologicalVertex."

        assert first_vertex != second_vertex, f"Cannot glue {self.self_edge} to the same vertex of edge {edge_to_glue}."
        assert edge_to_glue in first_vertex.parent_edges, f"Vertex {first_vertex} is not a child vertex of edge {edge_to_glue}."
        assert edge_to_glue in second_vertex.parent_edges, f"Vertex {second_vertex} is not a child vertex of edge {edge_to_glue}."

        self.edge_glued = edge_to_glue
        self.edge_glued_first_vertex = first_vertex
        self.edge_glued_second_vertex = second_vertex

        flipped = (first_vertex != edge_to_glue.v0) # If the orientation is flipped in the gluing, this needs to be reflected in the other gluing
        if not flipped:
            if not (edge_to_glue.edge_glued.edge_glued == self.self_edge and edge_to_glue.edge_glued.edge_glued_first_vertex == self.self_edge.v0 and edge_to_glue.edge_glued.edge_glued_second_vertex == self.self_edge.v1):
                # Only perform this operation if the gluing actually changes the current topological configuration.
                edge_to_glue.edge_glued.glue_edge(self.self_edge, self.self_edge.v0, self.self_edge.v1)
        else:
            if not (edge_to_glue.edge_glued.edge_glued == self.self_edge and edge_to_glue.edge_glued.edge_glued_first_vertex == self.self_edge.v1 and edge_to_glue.edge_glued.edge_glued_second_vertex == self.self_edge.v0):
                # Only perform this operation if the gluing actually changes the current topological configuration.
                edge_to_glue.edge_glued.glue_edge(self.self_edge, self.self_edge.v1, self.self_edge.v0)
    
    def get_edge(self):
        return self.edge_glued
    def get_glued_first_vertex(self):
        return self.edge_glued_first_vertex
    def get_glued_second_vertex(self):
        return self.edge_glued_second_vertex

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
    """
    TopologicalEdge object which defines the 1-dim skeleton of a topological space.
    The edge is given a natural orientation in the order v0 -> v1, where v0, v1 are its adjacent (viewed as children) vertices.
    """
    def __init__(self, v0, v1, uid=0):
        assert isinstance(v0, TopologicalVertex), f"Vertex {v0} is not a valid TopologicalVertex."
        assert isinstance(v1, TopologicalVertex), f"Vertex {v1} is not a valid TopologicalVertex."
        
        assert v0 != v1, "Can't assign the same vertex to the endpoints of edge."
        self.v0 = v0
        self.v1 = v1
        self.vertices = [v0,v1]
        for v in self.vertices:
            v.add_parent_edge(self)
        self.uid = uid
        self.parent_polyons = []
        self.neighbouring_edges = {v0: [], v1: []} # Hash map for all neighbouring edges connected at v0 or v1
        self.edge_glued = EdgeGluing(self)
    
    def add_neighbouring_edge(self, neighbour_edge, common_vertex):
        """
        Adds a neighbouring edge to this edge at a common vertex.
        """
        assert isinstance(neighbour_edge, TopologicalEdge), f"Edge {neighbour_edge} is not a valid TopologicalEdge."
        assert isinstance(common_vertex, TopologicalVertex), f"Vertex {common_vertex} is not a valid TopolgicalVertex."
        assert neighbour_edge in common_vertex.parent_edges, f"Vertex {common_vertex} is not a child vertex of edge {neighbour_edge}."
        assert self in common_vertex.parent_edges, f"Vertex {common_vertex} is not a child vertex of edge {neighbour_edge}."
        
        if neighbour_edge not in self.neighbouring_edges:
            self.neighbouring_edges[common_vertex].append(neighbour_edge)
        
        neighbour_edge.add_neighbouring_edge(self, common_vertex)

    def change_v0(self, new_v0):
        self.v0 = new_v0
        self.neighbouring_edges[new_v0] = self.neighbouring_edges.pop()
    
    def change_v1(self, new_v1):
        self.v1 = new_v1
        self.neighbouring_edges[new_v1] = self.neighbouring_edges.pop()


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


    
    def auto_index_children(self):
        """
        Automatically adds indices for the children at the Polygon level, because every polygon gives relative indices to their own edges and vertices.
        """
        for edge in self.edges:
            assert isinstance(edge, TopologicalEdge), f"Edge {edge} is not a valid TopologicalEdge."
    
    def add_disjoint_edge(self, edge):
        assert isinstance(edge, TopologicalEdge), f"Edge {edge} is not a valid TopologicalEdge."
        assert edge not in self.edges, f"Edge {edge} is already an edge of polygon {self}."
        self.edges.append(edge)
        edge.add_parent_polygon(self)
    
    def add_vertex_connected_edge(self, new_edge, connecting_edge, common_vertex):
        assert isinstance(new_edge, TopologicalEdge), f"Edge {new_edge} is not a valid TopologicalEdge."
        assert isinstance(connecting_edge, TopologicalEdge), f"Edge {connecting_edge} is not a valid TopologicalEdge."
        assert isinstance(common_vertex, TopologicalVertex), f"Vertex {common_vertex} is not a valid TopologicalVertex."

        assert connecting_edge in self.edges, f"Edge {connecting_edge} is not a valid child edge of polygon {self}."
        assert new_edge not in self.edges, f"Edge {new_edge} is already an edge in polygon {self}."

        new_edge.add_neighbouring_edge(connecting_edge, common_vertex)
        self.edges.append(connecting_edge)
        connecting_edge.add_parent_polygon(self)

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
        self.add_disjoint_edge(edge)

class TopologicalTriangle(TopologicalPolygon):
    """
    Triangle class which is an inherited TopologicalPolygon with added functionality such as canonical indexing.
    """
    def __init__(self, uid=0):
        super().__init__()
    
    def add_disjoint_edge(self, edge):
        assert len(self.edges) <= 2, f"Triangle {self} cannot have more than 3 edges."
        return super().add_disjoint_edge(edge)
    
    def add_vertex_connected_edge(self, new_edge, connecting_edge, common_vertex):
        assert len(self.edges) <= 2, f"Triangle {self} cannot have more than 3 edges."
        return super().add_vertex_connected_edge(new_edge, connecting_edge, common_vertex)

    

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
            
    
    
