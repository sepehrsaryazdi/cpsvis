"""

This module is dedicated for creating new GUI widgets of various functionality.

"""

import tkinter as tk

class GUIWindow:
    def __init__(self, root, title):
        self.root = root
        self.window = tk.Toplevel()
        self.window.wm_title(title)
        l = tk.Label(self.window, text="Enter the desired genus g and number of punctures n for the surface Sg,n below.")
        l.pack(padx=20, pady=10)
        g_input_frame = tk.Frame(self.window)
