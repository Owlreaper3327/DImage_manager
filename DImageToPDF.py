"""This is the user interface for the program, that will use the logic from the main class
ConversionManager"""

import _tkinter
import tkinter as tk
import customtkinter as ctk
from converter.conversion import TaskManager
from converter import utils
from gui.app_main_gui import DImage

app = DImage()
app.mainloop()
