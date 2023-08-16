
"""
This module allows conversion between the gluing table representation and a TopologicalMultiTriangle.
"""

from cpsvis.core.topology import TopologicalMultiTriangle, TopologicalTriangle, TopologicalEdge, TopologicalVertex
from cpsvis.vis.combinatorial_map import CombinatorialAlgorithm
import pandas as pd
import numpy as np
from tkinter import ttk, messagebox


class GluingTableConversion:

    def gluing_table_to_topological_multi_triangle(gluing_table) -> TopologicalMultiTriangle:
        assert isinstance(gluing_table, pd.DataFrame)
        pass

    def parse_edge_identification(row,col,value, dataframe) -> tuple[str, str, str, str]:
        """
        Parses edge identification
        
        """
        assert isinstance(row, int), f"Row {row} is not a valid int."
        assert isinstance(col, int), f"Col {col} is not a valid int."
        assert isinstance(value, str), f"Value {value} is not a valid string."
        assert isinstance(dataframe, pd.DataFrame), f"Dataframe {dataframe} is not a valid Pandas dataframe."

    
        triangle_index, edge_bracket = value.rsplit(" ")
        second_triangle_index = str(triangle_index)
        
        assert edge_bracket.count("(") == 1 and edge_bracket.count(")") == 1, f"One or more brackets are misplaced."
        second_edge_index = edge_bracket.rsplit("(")[1].rsplit(")")[0]

        
        column_name = dataframe.columns[col]
        first_edge_index = column_name.rsplit("(")[1].rsplit(")")[0]
        first_triangle_index = str(dataframe.index[row])
        
        return (first_triangle_index, first_edge_index, second_triangle_index, second_edge_index)

    def convert_index_increasing_order(string) -> str:
        assert isinstance(string, str), f"String {string} is not a valid str."
        indices = [int(i) for i in string]
        indices.sort()
        indices = [str(i) for i in indices]
        return "".join(indices)
    
    # def convert_vertices_anticlockwise_order(edge_vertices, edge_index) -> tuple[TopologicalVertex, TopologicalVertex]:
    #     """
    #     Sorts the edge's vertices in the same way as the sorting of the edge index.
    #     """
        
    #     assert isinstance(edge_index, str), f"Edge index {edge_index} is not a valid str."
    #     indices = np.array([int(i) for i in edge_index])
        
    #     sorting_indices = np.argsort(indices)
    #     indices.sort()
    #     indices = [str(i) for i in indices]
    #     sorted_edges = np.array(edge_vertices)[sorting_indices]
    #     if "".join(indices) == "02":
    #         return (sorted_edges[1], sorted_edges[0])
    #     else:
    #         return (sorted_edges[0], sorted_edges[1])

    def get_vertices_in_index_order(triangle, edge, desired_index) -> tuple[TopologicalVertex, TopologicalVertex]:
        assert isinstance(triangle, TopologicalTriangle), f"Triangle {triangle} is not a valid TopologicalTriangle."
        assert isinstance(edge, TopologicalEdge), f"Edge {edge} is not a valid TopologicalEdge."
        assert isinstance(desired_index, str), f"Desired index {desired_index} is not a valid str."

        indices = [i for i in desired_index]
        vertices = edge.vertices
        vertices_desired_order = [triangle.index_to_vertex_hash[index] for index in indices]
        
        for v in vertices_desired_order:
            assert v in vertices, f"Vertex {v} is not a child vertex of edge {edge}."

        return vertices_desired_order

    
    def edge_gluing_flipped(first_edge_index, second_edge_index):
        assert isinstance(first_edge_index, str), f"First edge index {first_edge_index} is not a valid str."
        assert isinstance(second_edge_index, str), f"Second edge index {second_edge_index} is not a valid str."

        increasing_to_anticlockwise_form = {"01":"01", "12":"12", "02":"20"}

        first_edge_index_increasing = GluingTableConversion.convert_index_increasing_order(first_edge_index)
        second_edge_index_increasing = GluingTableConversion.convert_index_increasing_order(second_edge_index)

        flipped = (second_edge_index != increasing_to_anticlockwise_form[second_edge_index_increasing])

        return flipped

    def update_triangulation_gluing(first_triangle_index, first_edge_index, second_triangle_index, second_edge_index, triangulation):
        assert isinstance(first_edge_index, str), f"First triangle index {first_triangle_index} is not a valid int."
        assert isinstance(first_edge_index, str), f"First edge index {first_edge_index} is not a valid int."
        assert isinstance(second_triangle_index, str), f"Second triangle index {second_edge_index} is not a valid int."
        assert isinstance(second_edge_index, str), f"Second edge index {second_edge_index} is not a valid str."
        assert isinstance(triangulation, TopologicalMultiTriangle), f"Triangulation {triangulation} is not a valid TopologicalMultiTriangle."

        assert first_triangle_index != second_triangle_index, f"Cannot glue triangle {first_triangle_index} to itself. Please glue this to a different triangle."

        first_triangle = triangulation.index_to_polygon_hash[first_triangle_index]
        assert isinstance(first_triangle, TopologicalTriangle), f"First triangle {first_triangle} is not a valid TopologicalTriangle."
        
        first_edge_index_increasing = GluingTableConversion.convert_index_increasing_order(first_edge_index)
        first_triangle_increasing_hash = first_triangle.edge_index_increasing_hash()
        assert first_edge_index_increasing in first_triangle_increasing_hash.keys(), f"First edge index {first_edge_index} is not a valid edge index for triangle {first_triangle_index}."
        first_edge = first_triangle.index_to_edge_hash[first_triangle_increasing_hash[first_edge_index_increasing]]
        assert isinstance(first_edge, TopologicalEdge), f"First edge {first_edge} is not a valid TopologicalEdge."

        assert (second_triangle_index in triangulation.index_to_polygon_hash.keys()), f"Triangle index {second_triangle_index} is not a valid index."
        second_triangle = triangulation.index_to_polygon_hash[second_triangle_index]
        assert isinstance(second_triangle, TopologicalTriangle), f"Second triangle {second_triangle} is not a valid TopologicalTriangle."
    
        second_edge_index_increasing = GluingTableConversion.convert_index_increasing_order(second_edge_index)
        second_triangle_increasing_hash = second_triangle.edge_index_increasing_hash()
        assert (second_edge_index_increasing in second_triangle_increasing_hash.keys()), f"Edge index {second_edge_index} is not a valid edge index for triangle {second_triangle_index}."
        second_edge = second_triangle.index_to_edge_hash[second_triangle_increasing_hash[second_edge_index_increasing]]
        assert isinstance(second_edge, TopologicalEdge), f"Second edge {second_edge} is not a valid TopologicalEdge."


        first_edge_vertices = GluingTableConversion.get_vertices_in_index_order(first_triangle, first_edge, first_edge_index)
        second_edge_vertices = GluingTableConversion.get_vertices_in_index_order(second_triangle, second_edge, second_edge_index)

        # print([first_triangle.vertex_to_index_hash[v] for v in first_edge_vertices])

        # print([second_triangle.vertex_to_index_hash[v] for v in second_edge_vertices])

        first_edge.edge_glued.glue_edge(second_edge, first_edge_vertices[0], first_edge_vertices[1], second_edge_vertices[0], second_edge_vertices[1])
        
        
        print(CombinatorialAlgorithm.spanning_polygon_tree(triangulation.polygons[0], [], []))
        # print(first_triangle, first_edge, second_triangle, second_edge)

        # GluingTableConversion.edge_gluing_flipped(first_edge_index, second_edge_index)
        # first_edge_sorted_vertices = GluingTableConversion.convert_vertices_anticlockwise_order((first_edge.v0, first_edge.v1), first_edge_index)
        # second_edge_sorted_vertices =  GluingTableConversion.convert_vertices_anticlockwise_order((second_edge.v0, second_edge.v1), second_edge_index)

        # print(first_edge_index,first_edge_sorted_vertices == (first_edge.v0, first_edge.v1))


        # first_edge.edge_glued.glue_edge(second_edge, first_edge_sorted_vertices[0], first_edge_sorted_vertices[1], second_edge_sorted_vertices[0], second_edge_sorted_vertices[1])
