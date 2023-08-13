
"""
This module allows conversion between the gluing table representation and a TopologicalMultiTriangle.
"""

from cpsvis.core.topology import TopologicalMultiTriangle
import pandas as pd

class GluingTableConversion:

    def gluing_table_to_topological_multi_triangle(gluing_table) -> TopologicalMultiTriangle:
        assert isinstance(gluing_table, pd.DataFrame)
        pass