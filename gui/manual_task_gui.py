
from customtkinter import *
from PIL import Image
from converter.task_builders import ManualTaskBuilder, MergeTaskBuilder

class ManualTaskWindow(CTkToplevel):

    task: ManualTaskBuilder

    def __init__(self, callback:function, mode="manual"):
        super().__init__()

        self.file_line = CTkScrollableFrame(master=self, orientation="vertical", border_width=3, height=380, width=270)
        self.file_line.pack(pady=(0, 55), side="right")
        self.button_frame = CTkFrame(master=self, height=230)
        self.button_frame.pack_propagate(False)
        self.button_frame.pack(pady=(0, 200), side="left")
        self.add_file = CTkButton(master=self.button_frame, text="Add file")
        self.add_file.pack()
        self.clean = CTkButton(master=self.button_frame, text="Clean files")
        self.clean.pack(pady=(8, 0))
        self.accept = CTkButton(master=self.button_frame, text="Accept")
        self.accept.pack(pady=(8, 0))
        self.final_name = CTkEntry(master=self.button_frame, placeholder_text="Introduce final filename")
        self.final_name.pack(pady=(8, 0))
        self.accept_name = CTkButton(master=self.button_frame, text="Accept name")
        self.accept_name.pack(pady=(8, 0))
        self.cancel = CTkButton(master=self.button_frame, text="Cancel", fg_color=("#ff1919", "#ff0000"), hover_color=("#c20000", "#800000"))
        self.cancel.pack(pady=(16, 0))

        self._set_appearance_mode("dark-blue")
        self.geometry("500x450")
        self.title("Manual task")
        self.configure(fg_color=['gray92', 'gray14'])

        if mode == "manual":
            self.task = ManualTaskBuilder()
        else:
            self.task = MergeTaskBuilder()
        
        self.data_send = callback