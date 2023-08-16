"""
This module defines functions which visualise a combinatorial map, expecting a TopologicalMultiPolygon which returns a matplotlib plot which visualises this.
"""

from cpsvis.core.topology import TopologicalMultiPolygon, TopologicalEdge, TopologicalVertex, TopologicalPolygon

class CombinatorialAlgorithm:


    def spanning_polygon_tree(polygon, discovered_list, edge_connection) -> tuple[list,list]:
        """
        Computes a spanning tree, starting with polygon.
        """
        discovered_list.append(polygon)
        assert isinstance(polygon, TopologicalPolygon), f"Polygon {polygon} is not a valid TopologicalPolygon."
        for edge in polygon.edges:
            assert isinstance(edge, TopologicalEdge), f"Edge {edge} is not a valid TopoloigcalEdge."
            if edge.edge_glued.edge_glued != None:
                new_polygon = edge.edge_glued.edge_glued.parent_polyons[0]
                if new_polygon not in discovered_list:
                    edge_connection.append(edge)
                    discovered_list, edge_connection = CombinatorialAlgorithm.spanning_polygon_tree(new_polygon, discovered_list,edge_connection)
        return discovered_list, edge_connection
            


    
    def spanning_polygon_forest(multi_polygon):
        assert isinstance(multi_polygon, TopologicalMultiPolygon), f"Multi polygon {multi_polygon} is not a valid TopologicalMultiPolygon."


