"""Script to contain the app gui made with ctk into classes"""

import customtkinter as ctk
import os

import function

from converter.conversion import TaskManager
from converter.task_builders import AutoTaskBuilder, ManualTaskBuilder, MergeTaskBuilder, \
    NonReadyTaskException
from converter.conversion import AutoConversionTask, ManualConversionTask
from converter import utils

class ManualTaskWindow(ctk.CTkToplevel):
    """Class that serves to render the gui for manual and merge task builders"""



    def __init__(self, callback:function, mode:str="manual"):
        super().__init__()

        if mode != "manual":
            self.task = MergeTaskBuilder()
        else:
            self.task = ManualTaskBuilder()
        
        self.exit_call = callback
        
        self.geometry("800x600")

        self.select_file = ctk.CTkButton(self, command=self.select_file_callback, 
                                         text="Select file")
        self.select_file.grid(column= 0, row=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

        self.select_dest_folder = ctk.CTkButton(self, command=self.select_folder_callback, 
                                                text="Select a folder")
        self.select_dest_folder.grid(column=0, row=1, padx = (0,10), pady=(10,0), sticky="nsew")
        self.final_name = ctk.CTkEntry(self)
        self.final_name.grid(column=0, row=2, padx=(0,20),pady=(20,0), sticky="nsew")
        
        self.send_name = ctk.CTkButton(self, command=self.set_name,
                                       text="Set filename")

        self.accept = ctk.CTkButton(self, command=self.accpet_callback,
                                    text="Accept")
        self.accept.grid(column=1, row=3, padx=(0,10), pady=(10,0), sticky="nsew")


    def select_folder_callback(self):
        """Callback function for the button to select a file"""

        folder = ctk.filedialog.askdirectory(initialdir=os.getcwd(), mustexist=True,
                                             title="Select a folder")

        if folder:
            try:
                self.task.set_destination_folder(folder)
            except AttributeError as ate:
                print(ate)
    
    def accpet_callback(self):
        """Callback for the accept button"""

        task:ManualConversionTask

        try:
            task = self.task.get_task()
        
        except NonReadyTaskException as norte:
            print(norte)
        
        self.exit_call(task)
        self.destroy()
    
    def select_file_callback(self):
        """Select file to append to the file queue"""

        file = ctk.filedialog.askopenfilename(initialdir=os.getcwd(), 
                                              filetypes=(".png",".jpg",".webp",".jpeg"))

        if file:
            self.task.add_file(file)
    
    def set_name(self):
        """Callback to set the final name of the task"""

        tes = self.final_name.get()

        if tes:
            if not tes.endswith(".pdf"):
                tes = tes + ".pdf"



class DImage(ctk.CTk):
    """Class that serves as the custom implementation for CustomTkinter for my app"""

    task_manager: TaskManager

    def __init__(self):
        super().__init__()

        self.task_manager = TaskManager()
        self.geometry("800x600")

        self.manual_conversion = ctk.CTkButton(self, 
                        command=self.open_manual, text="Manual Conversion")
        self.manual_conversion.grid(column=0, row=0, padx=(0,10), pady=(10,0), sticky="ew")

        #Unfinished


    def open_manual(self):
        """Callback to open manual conversion window"""

        sec = ManualTaskWindow(self.recieve_task)

        sec.grab_set()
        sec.transient()
        sec.wait_window()
    
    def recieve_task(self, task:ManualConversionTask):
        """Callback that recieves and add the task to the task manager"""

        self.task_manager.add_other_task(task)
