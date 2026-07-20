
import os
from customtkinter import *
from tkinter import messagebox as msb
from PIL import Image
from converter.task_builders import ManualTaskBuilder, MergeTaskBuilder,\
    NonReadyTaskException
from converter.conversion import ManualConversionTask

class FileGUI(CTkFrame):
    """Class to show the added files on manual tasks"""

    def __init__(self, master:ManualTaskWindow, file:str):
        super().__init__(master=master.file_line, bg_color="#f5e231",
                         width=250)

        name = os.path.basename(file)
        self.master_d = master
        self.file = file

        self.filename = CTkLabel(master=self,
                                 text=name, bg_color="#c3ffee")
        self.filename.pack(side="left")

        self.delete_button = CTkButton(master=self,
                                       text="Delete",
                                       command=self.delete_file)
        self.delete_button.pack(side="left")
    
    def delete_file(self):
        """Callback for the files delete button"""

        self.master_d.task.task.files.remove(self.file)
        self.destroy()


class ManualTaskWindow(CTkToplevel):

    task: ManualTaskBuilder
    file_list:list[FileGUI]

    def __init__(self, master, mode="manual", task:ManualConversionTask = None):
        super().__init__()

        self.file_line = CTkScrollableFrame(master=self, 
                                            orientation="vertical", 
                                            border_width=3, 
                                            height=380, width=270)
        self.file_line.pack(pady=(0, 55), side="right")
        self.button_frame = CTkFrame(master=self, height=270)
        self.button_frame.pack_propagate(False)
        self.button_frame.pack(pady=(0, 160), side="left")
        
        self.select_dest_folder = CTkButton(master=self.button_frame,
                                            text="Select destination folder",
                                            command=self.select_folder_callback)
        self.select_dest_folder.pack()

        self.add_file = CTkButton(master=self.button_frame, 
                                  text="Add file",
                                  command=self.add_file_callaback)
        self.add_file.pack(pady=(8, 0))
        self.clean = CTkButton(master=self.button_frame,
                               text="Clean files",
                               command=self.clean_files_callback)
        self.clean.pack(pady=(8, 0))
        self.accept = CTkButton(master=self.button_frame, 
                                text="Accept",
                                command=self.accept_task)
        self.accept.pack(pady=(8, 0))
        self.final_name = CTkEntry(master=self.button_frame, 
                                   placeholder_text="Introduce final filename")
        self.final_name.pack(pady=(8, 0))
        self.accept_name = CTkButton(master=self.button_frame, 
                                     text="Accept name",
                                     command=self.set_final_name)
        self.accept_name.pack(pady=(8, 0))
        self.cancel = CTkButton(master=self.button_frame, 
                                text="Cancel", 
                                fg_color=("#ff1919", "#ff0000"), 
                                hover_color=("#c20000", "#800000"),
                                command=self.cancel_callback)
        self.cancel.pack(pady=(16, 0))


        self.file_list = []

        self._set_appearance_mode("dark-blue")
        self.geometry("500x450")
        self.title("Manual task")
        self.configure(fg_color=['gray92', 'gray14'])

        if mode == "manual":
            self.task = ManualTaskBuilder()
        else:
            self.task = MergeTaskBuilder()
        
        if task is not None:
            self.task.task = task
        
        self.master_d = master
    
    def add_file_callaback(self):
        """Callback for the add file button"""

        file = filedialog.askopenfilename(initialdir=os.getcwd())
        
        if file:
            try:
                self.task.add_file(file)
                file_gui = FileGUI(self, file)
                self.file_list.append(file_gui)
                file_gui.pack()
            
            except AttributeError as ate:
                msb.showerror("Error", ate)
    
    def clean_files_callback(self):
        """Callback for the clean files button"""

        for file_gui in self.file_list:

            file_gui.delete_file()
    
    def accept_task(self):
        """Callback to accept button"""

        try:

            task = self.task.get_task()

            self.master_d.pass_task(task)
            self.destroy()
        
        except NonReadyTaskException as norte:
            msb.showerror("Error", norte)
    
    def select_folder_callback(self):
        """Callback to select folder button"""

        folder = filedialog.askdirectory(initialdir=os.getcwd(), 
                                         mustexist=True)
        
        if folder:
            self.task.set_destination_folder(folder)
    
    def set_final_name(self):
        """Callback for the accept name button"""

        final_n = self.final_name.get()

        if final_n:

            self.task.set_final_name(final_n)
        
        else:
            msb.showwarning("Warning", "Final name entry is empty")
    
    def cancel_callback(self):
        """Callback for the cancel button"""

        del(self.file_line)
        del(self.task)

        self.destroy()