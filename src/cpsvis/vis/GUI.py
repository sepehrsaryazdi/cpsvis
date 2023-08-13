"""

This module is dedicated for creating new GUI widgets of various functionality.

"""

import tkinter as tk


class MenuBar:
    def __init__(self, root):
        assert isinstance(root, tk.Tk), f"Root {root} is not a valid tk.Tk object."
        self.root = root
        self.tk_menu_bar = tk.Menu(root)
    
    def add_menu(self, menu) -> None:
        assert isinstance(menu, Menu), f"Menu {menu} is not a valid Menu."
        self.tk_menu_bar.add_cascade(label=menu.label, menu=menu.tk_menu)
    
    def attach_menu_bar(self) -> None:
        self.root.configure(menu=self.tk_menu_bar)

class Menu:
    def __init__(self, menu_bar, label):
        assert isinstance(label, str), f"Label {label} is not a valid str."
        assert isinstance(menu_bar, MenuBar), f"Menubar {menu_bar} is not a valid MenuBar."
        self.tk_menu = tk.Menu(menu_bar.tk_menu_bar, tearoff=0)
        self.label = label
    
    def add_dropdown_option(self, label, callback_fn) -> None:
        assert isinstance(label, str), f"Label {label} is not a valid str."
        assert callable(callback_fn), f"Callback function {callback_fn} is not a valid function."
        self.tk_menu.add_command(label=label, command=callback_fn)

class GUIWindow:
    def __init__(self, root, title, width=1280, height=520):
        assert isinstance(root, tk.Tk), f"Root {root} is not a valid tk.Tk object."
        assert isinstance(title, str), f"Title {title} is not a valid str."
        assert isinstance(width, int), f"Width {width} is not a valid integer."
        assert isinstance(height, int), f"Height {height} is not a valid integer."
        self.root = root
        self.window = tk.Toplevel()
        self.window.wm_title(title)
        self.window.geometry(f"{width}x{height}")
        # l = tk.Label(self.window, text="Enter the desired genus g and number of punctures n for the surface Sg,n below.")
        # l.pack(padx=20, pady=10)
        # g_input_frame = tk.Frame(self.window)

