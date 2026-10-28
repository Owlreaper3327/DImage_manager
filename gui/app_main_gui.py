"""Main GUI for the app"""

import os
import time
from tkinter import messagebox as msb
from customtkinter import *
from PIL import Image
from converter.conversion import TaskManager, ConversionTask, AutoConversionTask,\
ManualConversionTask
from converter.task_builders import ManualTaskBuilder, MergeTaskBuilder, NonReadyTaskException
from converter import utils
from gui.auto_task_gui import AutoTaskWindow
from gui.manual_task_gui import ManualTaskWindow

class TaskGUI(CTkFrame):
    """GUI to represent the tasks"""

    def __init__(self, master: DImage, task_id: ConversionTask):
        super().__init__(master=master.queue_frame, bg_color="#a8e8fd")

        self.master_d = master
        self.task_id = task_id
        
        self.task_name = CTkLabel(master=self,
                                  text=self.task_id.final_name, 
                                  text_color="#000000",
                                  bg_color="#a8e8fd")
        self.task_name.pack(side="left")
        
        mode = self.task_id.mode.capitalize()
        self.task_type = CTkLabel(master=self,
                                  text=mode, 
                                  text_color="#ffffff",
                                  bg_color="#4cecdf")
        self.task_type.pack(side="left")
        self.delete_button = CTkButton(master=self,
                                       text="Delete",
                                       command=self.delete_task,
                                       height=40, width=40,
                                       text_color="#ffffff",
                                       bg_color="#ff0000")
        self.delete_button.pack(side="left")
        self.status = CTkLabel(master=self,
                               bg_color="#ffea00",
                               width=10, height=10, 
                               text="")
        self.status.pack(side="left")

    

    def delete_task(self):
        """Callback to delete tasks"""

        self.master_d.task_manager.remove_from_queue(self.task_id)
        self.master_d.task_gui_queue.remove(self)

        self.destroy()
    
    def update_status(self, n_t:int = 3):
        """Function to update the color status of task"""

        if n_t == 1:
            self.status.configure(require_redraw=True, bg_color="#00ff37") 
        elif n_t == 2:
            self.status.configure(require_redraw=True, bg_color="#ff0000")
        else:
            self.status.configure(require_redraw=True, bg_color="#0022ff")

class DImage(CTk):

    task_manager: TaskManager
    task_gui_queue: list[TaskGUI]

    def __init__(self):
        super().__init__()

        self.task_manager = TaskManager()

        self.task_frame = CTkScrollableFrame(master=self, 
                                             orientation="vertical", width=190)
        self.task_frame.pack(expand=1, padx=(10, 0), 
                             pady=(0, 250), side="left")
        self.manual_conversion_b = CTkButton(master=self.task_frame, 
                                           text="Manual conversion", 
                                           command=self.manual_conversion)
        self.manual_conversion_b.pack()
        self.merge_conversion = CTkButton(master=self.task_frame, 
                                          text="Merge",
                                          command=self.merge_task)
        self.merge_conversion.pack(pady=(8, 0))
        self.auto_conversion = CTkButton(master=self.task_frame, 
                                         text="Auto-Conversion",
                                         command=self.auto_task)
        self.auto_conversion.pack(pady=(8, 0))
        self.rec_folder = CTkButton(master=self.task_frame, 
                                        text="Recursive Folder Conversion",
                                        command=self.auto_folder_task)
        self.rec_folder.pack(pady=(8, 0))
        self.queue_frame = CTkScrollableFrame(master=self, 
                                              orientation="vertical", 
                                              width=246, height=450, 
                                              corner_radius=6, border_width=3)
        self.queue_frame.pack(fill="x", pady=(3, 0))
        self.button_frame = CTkFrame(master=self, height=30, width=250)
        self.button_frame.pack_propagate(False)
        self.button_frame.pack(pady=(8, 0))
        self.cancel_button = CTkButton(master=self.button_frame, 
                                       text="Cancel", anchor="center", 
                                       width=125, command=self.cancel)
        self.cancel_button.pack(side="left")
        self.begin_button = CTkButton(master=self.button_frame, 
                                      text="Begin", width=125, command=self.start)
        self.begin_button.pack()

        self._set_appearance_mode("dark")
        self.geometry("500x520")
        self.title("DImage")
        self.configure(fg_color=['gray92', 'gray14'])

        self.task_gui_queue = []

        return

    def start(self):
        """Callback for begin button"""

        for task_g in self.task_gui_queue:

            task_g.update_status()

            status = self.task_manager.process_first()

            if status:
                task_g.update_status(1)
            else:
                task_g.update_status(2)

        msb.showinfo("Success", "Task queue has been completed")
    
    def cancel(self):
        """Callback for cancel button"""

        self.destroy()
    
    def pass_task(self, task:ConversionTask):
        """Delegate used to pass the tasks from the popup windows"""

        self.task_manager.add_other_task(task)
        self.__add_task_gui__(task)
    
    def pass_auto(self, task:str):
        """Function used to pass the auto task from the popup"""

        n_task = self.task_manager.create_auto_task(task)
        self.__add_task_gui__(n_task)
    
    def manual_conversion(self):
        """Callback for the manual conversion task window"""

        man_win = ManualTaskWindow(self)
        man_win.grab_set()
        man_win.wait_window()
    
    def auto_task(self):
        """Callback for the auto conversion task window"""

        aut_win = AutoTaskWindow(self)
        aut_win.grab_set()
        aut_win.wait_window()
    
    def merge_task(self):
        """Callback for the merge conversion task window"""

        mer_win = ManualTaskWindow(self, "merge")
        mer_win.grab_set()
        mer_win.wait_window()
    
    def auto_folder_task(self):
        """Callback for the recursive folder conversion task"""
        was_added = 0

        fold = filedialog.askdirectory(initialdir=os.getcwd, mustexist=True)

        if fold:
            task_list = utils.extract_queue(fold)
            
            for task in task_list:
                self.pass_auto(task)
                was_added += 1

        if was_added < 1:
            msb.showwarning("Warning","No tasks added to list")
        else:
            msb.showinfo("Info",f"{was_added} tasks added succesfully")
    
    def __add_task_gui__(self, task:ConversionTask):
        """Method to create the task queue in the gui"""

        gui = TaskGUI(self, task)

        self.task_gui_queue.append(gui)
        gui.pack()