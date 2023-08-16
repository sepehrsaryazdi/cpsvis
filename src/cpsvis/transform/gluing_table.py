
"""
This module allows conversion between the gluing table representation and a TopologicalMultiTriangle.
"""

from cpsvis.core.topology import TopologicalMultiTriangle
import pandas as pd
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

    def update_triangulation_gluing(first_triangle_index, first_edge_index, second_triangle_index, second_edge_index, triangulation):
        assert isinstance(first_edge_index, str), f"First triangle index {first_triangle_index} is not a valid int."
        assert isinstance(first_edge_index, str), f"First edge index {first_edge_index} is not a valid int."
        assert isinstance(second_triangle_index, str), f"Second triangle index {second_edge_index} is not a valid int."
        assert isinstance(second_edge_index, str), f"Second edge index {second_edge_index} is not a valid str."
        assert isinstance(triangulation, TopologicalMultiTriangle), f"Triangulation {triangulation} is not a valid TopologicalMultiTriangle."

        assert first_triangle_index != second_triangle_index, f"Cannot glue triangle {first_triangle_index} to itself. Please glue this to a different triangle."

        first_triangle = triangulation.index_to_polygon_hash[first_triangle_index]

        assert (second_triangle_index in triangulation.index_to_polygon_hash.keys()), f"Triangle index {second_triangle_index} is not a valid index."

        second_triangle = triangulation.index_to_polygon_hash[second_triangle_index]
        print(first_triangle, second_triangle)
        