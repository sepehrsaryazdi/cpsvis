"""

This module defines an instance of the CPSVis application that handles all UI visualisation components.

"""

import tkinter as tk

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
        self.tk_app.mainloop()
        
        

