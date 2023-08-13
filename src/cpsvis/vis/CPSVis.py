"""

This module defines an instance of the CPSVis application that handles all UI visualisation components.

"""

import tkinter as tk
from cpsvis.vis.GUI import GUIWindow, Menu, MenuBar

class TkApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(anchor='nw')


class CPSVis():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Convex Projective Structure Visualisation Tool')
        self.root.geometry("1280x520")
        self.menubar = tk.Menu(self.root)
        self.root.configure(menu=self.menubar)
        self.tk_app = TkApp(self.root)
        
        self.menubar = MenuBar(self.root)
        self.filemenu = Menu(self.menubar, "File")
        self.menubar.add_menu(self.filemenu)
        self.menubar.attach_menu_bar()
        self.filemenu.add_dropdown_option("Test", lambda : print("hello"))
        # self.win = GUIWindow(self.root, "Enter Gluing Table")

        # print(self.win)


        self.tk_app.mainloop()
        
        

