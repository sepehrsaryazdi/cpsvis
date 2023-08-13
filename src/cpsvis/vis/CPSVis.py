"""

This module defines an instance of the CPSVis application that handles all UI visualisation components.

"""

from pandastable import Table
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

from cpsvis.vis.GUI import GUIWindow, Menu, MenuBar

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
        self.window = GUIWindow(root, "Construct Gluing Table")
        self.table_frame = tk.Frame(self.window.tk_window)
        self.table_frame.pack()
        self.gluing_table = Table(self.table_frame, enable_menus=False)
        self.gluing_table.show()

        button = ttk.Button(self.window.tk_window, text="Test")
        # button.place(relx=0.5, rely=0.5, anchor="center")

class CPSVis:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title('Convex Projective Structure Visualisation Tool')
        self.root.geometry("1280x520")
        self.menubar = tk.Menu(self.root)
        self.root.configure(menu=self.menubar)
        self.tk_app = TkApp(self.root)
        
        self.menubar = MenuBar(self.root)
        self.filemenu = Menu(self.menubar, "Generate")
        self.menubar.add_menu(self.filemenu)
        self.menubar.attach_menu_bar()
        self.filemenu.add_dropdown_option("Construct Gluing Table", lambda : GluingTableInterface(self.root))



        self.tk_app.mainloop()
        
        

