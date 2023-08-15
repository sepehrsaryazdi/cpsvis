"""

This module defines an instance of the CPSVis application that handles all UI visualisation components.

"""
import pkg_resources
from pandastable import Table, TableModel
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from cpsvis.core.topology import TopologicalMultiTriangle, TopologicalTriangle
from cpsvis.transform.gluing_table import GluingTableConversion
import os

import cpsvis
from cpsvis.vis.GUI import GUIWindow, Menu, MenuBar


class GluingTableModel(TableModel):
    def __init__(self, triangulation, dataframe=None):
        assert isinstance(dataframe, pd.DataFrame), f"Dataframe {dataframe} is not a valid pandas Dataframe."
        super().__init__(dataframe)

        assert isinstance(triangulation, TopologicalMultiTriangle), f"Triangulation {triangulation} is not a valid TopologicalMultiTriangle."
        self.triangulation = triangulation
    
    def getValueAt(self, row, col):
        assert isinstance(self.df, pd.DataFrame), f"Dataframe {self.df} is not a valid Dataframe."
        if row >= len(self.df.index):
            self.addRow()
        return super().getValueAt(row, col)
    
    def addRow(self):
        self.df.loc[len(self.df.index)] = [""]*len(self.df.columns)

        triangle = TopologicalTriangle()
        triangle.auto_add_three_edges()

        self.triangulation.add_disjoint_polygon(triangle)
        self.triangulation.auto_index_children()

    def deleteRow(self, row, unique=True):
        return_val = super().deleteRow(row, unique)
        self.triangulation.delete_polygon(self.triangulation.index_to_polygon_hash[str(row)])


        self.df.index = pd.Index([i for i in range(len(self.df))])
        return return_val
        
    def setValueAt(self, value, row, col, df=None):

        try:
            first_triangle_index, first_edge_index, second_triangle_index, second_edge_index = GluingTableConversion.parse_edge_identification(row,col,value, self.df)
            # print(first_triangle_index, first_edge_index, second_triangle_index, second_edge_index)
            
            GluingTableConversion.update_triangulation_gluing(first_triangle_index, first_edge_index, second_triangle_index, second_edge_index, self.triangulation)
        
            
            return super().setValueAt(f"{second_triangle_index} ({second_edge_index})", row, col, df)
        except Exception as e:
            e = str(e)
            if len(e) >= 1:
                e = e[0].capitalize() + e[1:]
            else:
                e = e[0].capitalize()
            messagebox.showinfo(title="Error", message=e)
        

    


class TkApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(anchor='nw')

class GluingTableInterface:
    """
    This class defines a graphical user interface for constructing a gluing table.
    """
    def __init__(self, root):
        assert isinstance(root, tk.Tk), f"Root {root} is not a valid tk.Tk object."
        self.root = root
        self.window = GUIWindow(root, "Construct Triangulation Gluing Table")
        self.triangulation = TopologicalMultiTriangle()

        

        self.buttons_frame = ttk.Frame(self.window.tk_window)
        self.buttons_frame.pack(side="top", fill='x')

        self.add_triangle_button = ttk.Button(self.buttons_frame, text="Add Triangle")
        self.add_triangle_button.pack(side="left", padx=(5,2.5), pady=(0,0))

        self.delete_triangle_button = ttk.Button(self.buttons_frame, text="Delete Selected Triangle")
        self.delete_triangle_button.pack(side="left", padx=(2.5,2.5), pady=(0,0))

        self.table_frame = tk.Frame(self.window.tk_window)
        self.table_frame.pack(fill='x')

        self.initial_dict = {"Edge (01)": [""], "Edge (12)": [""], "Edge (20)": [""]}

        self.initial_table = pd.DataFrame(self.initial_dict)
        # self.initial_table.set_index("Triangle")



        self.gluing_table = Table(self.table_frame, enable_menus=False, dataframe=self.initial_table)
        self.gluing_table.showIndex()

        triangle = TopologicalTriangle()
        triangle.auto_add_three_edges()

        self.triangulation.add_disjoint_polygon(triangle)
        self.triangulation.auto_index_children()
        self.gluing_table.model = GluingTableModel(self.triangulation,dataframe=self.initial_table)
        self.gluing_table.multiplerowlist = [0]
        self.gluing_table.redraw()
        self.add_triangle_button.bind("<ButtonPress>", lambda event : [self.gluing_table.model.addRow(), self.gluing_table.redraw()])
        self.delete_triangle_button.bind("<ButtonPress>", lambda event : [self.gluing_table.model.deleteRow(index) for index in self.gluing_table.multiplerowlist] + [self.gluing_table.redraw()])


        def callback(*args):
            # print(self.gluing_table.multiplerowlist)
            pass
            # messagebox.showinfo(title="Achtung", message="Achtung")

        self.window.tk_window.bind('<Return>', callback)

        self.gluing_table.expandColumns(50)
        self.gluing_table.show()

        self.initial_table = pd.DataFrame({"Edge (01)": ["1"], "Edge (12)": [""], "Edge (20)": [""]})

        # self.gluing_table.show()



        


class CPSVis:
    def __init__(self):
        self.root = ThemedTk(theme="arc", className='Convex Projective Structure Visualisation Tool')
        self.root.title('Convex Projective Structure Visualisation Tool')
        self.root.geometry("1280x520")

        images_path = pkg_resources.resource_filename('cpsvis', 'image/hyperbolic_plane.png')
        self.root.iconphoto(False, tk.PhotoImage(file=images_path))

        self.menubar = tk.Menu(self.root)
        self.root.configure(menu=self.menubar)
        self.tk_app = TkApp(self.root)
        
        self.menubar = MenuBar(self.root)
        self.filemenu = Menu(self.menubar, "Generate")
        self.menubar.add_menu(self.filemenu)
        self.menubar.attach_menu_bar()
        self.filemenu.add_dropdown_option("Construct Gluing Table", lambda : GluingTableInterface(self.root))



        self.tk_app.mainloop()
        
        

