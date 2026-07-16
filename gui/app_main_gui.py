"""Main GUI for the app"""

import os
from customtkinter import *
from PIL import Image
from converter.conversion import TaskManager, ConversionTask, AutoConversionTask,\
ManualConversionTask
from converter.task_builders import ManualTaskBuilder, MergeTaskBuilder, NonReadyTaskException
from converter import utils
from auto_task_gui import AutoTaskWindow
from manual_task_gui import ManualTaskWindow

class DImage(CTk):

    task_manager: TaskManager

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.task_manager = TaskManager()

        self.SCROLLABLEFRAME1 = CTkScrollableFrame(master=self, orientation="vertical", width=190)
        self.SCROLLABLEFRAME1.pack(expand=1, padx=(10, 0), pady=(0, 250), side="left")
        self.BUTTON2 = CTkButton(master=self.SCROLLABLEFRAME1, text="Manual conversion")
        self.BUTTON2.pack()
        self.BUTTON3 = CTkButton(master=self.SCROLLABLEFRAME1, text="Merge")
        self.BUTTON3.pack(pady=(8, 0))
        self.BUTTON4 = CTkButton(master=self.SCROLLABLEFRAME1, text="Auto-Conversion")
        self.BUTTON4.pack(pady=(8, 0))
        self.BUTTON5 = CTkButton(master=self.SCROLLABLEFRAME1, text="Default Folder Conversion")
        self.BUTTON5.pack(pady=(8, 0))
        self.SCROLLABLEFRAME6 = CTkScrollableFrame(master=self, orientation="vertical", width=246, height=450, corner_radius=6, border_width=3)
        self.SCROLLABLEFRAME6.pack(fill="x", pady=(3, 0))
        self.FRAME8 = CTkFrame(master=self, height=30, width=250)
        self.FRAME8.pack_propagate(False)
        self.FRAME8.pack(pady=(8, 0))
        self.BUTTON11 = CTkButton(master=self.FRAME8, text="Cancel", anchor="center", width=125)
        self.BUTTON11.pack(side="left")
        self.BUTTON12 = CTkButton(master=self.FRAME8, text="Begin", width=125)
        self.BUTTON12.pack()

        self._set_appearance_mode("dark")
        self.geometry("500x520")
        self.title("DImage")
        self.configure(fg_color=['gray92', 'gray14'])