
from customtkinter import *
from PIL import Image

class AutoTaskWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.action_frame = CTkFrame(master=self)
        self.action_frame.pack_propagate(False)
        self.action_frame.pack(pady=(0, 70), padx=(10, 0), side="left")
        self.select_folder = CTkButton(master=self.action_frame, text="Select folder")
        self.select_folder.pack(pady=(6, 0))
        self.final_name = CTkEntry(master=self.action_frame, placeholder_text="Enter the final name (optional)")
        self.final_name.pack(pady=(8, 0))
        self.accept_name = CTkButton(master=self.action_frame, text="Set final filename (optional)")
        self.accept_name.pack(pady=(8, 0))
        self.def_frame = CTkFrame(master=self, width=175, height=50)
        self.def_frame.pack_propagate(False)
        self.def_frame.pack(side="bottom")
        self.accept_task = CTkButton(master=self.def_frame, text="Accept", width=85)
        self.accept_task.pack(side="right")
        self.cancel = CTkButton(master=self.def_frame, text="Cancel", width=85)
        self.cancel.pack(side="right")

        self._set_appearance_mode("dark")
        self.geometry("400x300")
        self.title("Auto task")
        self.configure(fg_color=['gray92', 'gray14'])