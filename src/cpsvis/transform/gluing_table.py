
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

    def parse_edge_identification(row,col,value, dataframe) -> tuple[bool, dict]:
        """
        Parses edge identification
        
        """
        assert isinstance(row, int), f"Row {row} is not a valid int."
        assert isinstance(col, int), f"Col {col} is not a valid int."
        assert isinstance(value, str), f"Value {value} is not a valid string."
        assert isinstance(dataframe, pd.DataFrame), f"Dataframe {dataframe} is not a valid Pandas dataframe."

    
        triangle_index, edge_bracket = value.rsplit(" ")
        triangle_index = int(triangle_index)
        
        assert edge_bracket.count("(") == 1 and edge_bracket.count(")") == 1, f"One or more brackets are misplaced."
        second_edge_index = edge_bracket.rsplit("(")[1].rsplit(")")[0]

        print(triangle_index, second_edge_index)
        
        column_name = dataframe.columns[col]
        first_edge_index = column_name.rsplit("(")[1].rsplit(")")[0]
        
        return (True, {})

        