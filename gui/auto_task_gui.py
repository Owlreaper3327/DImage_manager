
import os
from customtkinter import *
from PIL import Image
from converter.conversion import AutoConversionTask
from tkinter import messagebox as msb

class AutoTaskWindow(CTkToplevel):

    task: AutoConversionTask


    def __init__(self, master):
        super().__init__()

        self.action_frame = CTkFrame(master=self)
        self.action_frame.pack_propagate(False)
        self.action_frame.pack(pady=(0, 70), padx=(10, 0), side="left", )
        self.select_folder = CTkButton(master=self.action_frame, 
                                       text="Select folder", 
                                       command=self.select_folder_callback)
        self.select_folder.pack(pady=(6, 0))
        self.final_name = CTkEntry(master=self.action_frame, placeholder_text="Enter the final name (optional)")
        self.final_name.pack(pady=(8, 0))
        self.accept_name = CTkButton(master=self.action_frame, 
                                     text="Set final filename (optional)",
                                     command=self.set_final_name_callback)
        self.accept_name.pack(pady=(8, 0))
        self.def_frame = CTkFrame(master=self, width=175, height=50)
        self.def_frame.pack_propagate(False)
        self.def_frame.pack(side="bottom")
        self.accept_task = CTkButton(master=self.def_frame, 
                                     text="Accept", width=85,
                                     command=self.accept_callback)
        self.accept_task.pack(side="right")
        self.cancel = CTkButton(master=self.def_frame, 
                                text="Cancel", width=85,
                                command=self.cancel_callback)
        self.cancel.pack(side="right")

        self._set_appearance_mode("dark")
        self.geometry("400x300")
        self.title("Auto task")
        self.configure(fg_color=['gray92', 'gray14'])

        self.master_d = master
        self.task = AutoConversionTask(final_name=None, mode="auto", 
                                       folder_path=None)
    
    def select_folder_callback(self):
        """Callback for select folder button"""

        folder = filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True)

        if folder:
            self.task.folder_path = folder
    
    def set_final_name_callback(self):
        """Callback for the set name button"""

        name = self.final_name.get()
        folder = self.task.folder_path

        if name and not (folder is None):
            
            if not name.endswith(".pdf"):
                name = name + ".pdf"

            full = os.path.join(folder, name)

            if not os.path.exists(full):
                self.task.final_name = name
            else:
                msb.showwarning("Warning", "The requested filename already exists")
        else:
            msb.showerror("Error", 
                          "Final name is empty or you haven't choose a destination folder")
    
    def accept_callback(self):
        """Callback for the button to accept the creation of new auto tasks"""

        folder = self.task.folder_path
        name = self.task.final_name

        if folder is None:
            msb.showerror("Error",
                          "Destination folder must be setted")
            return

        if name is None:

            self.master_d.pass_auto(folder)
            self.destroy()
            return
        
        self.master_d.pass_task(self.task)
        self.destroy()
    
    def cancel_callback(self):
        """Callback for cancel button"""

        self.destroy()