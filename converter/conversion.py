"""Script that contains the classes for conversion"""

import img2pdf
import os
import pypdf
from dataclasses import dataclass
from pypdf import PdfReader, PdfWriter
from . import utils

@dataclass
class ConversionTask:
    """Base class to all the oncoming types of tasks"""

    final_name:str
    mode:str

@dataclass
class AutoConversionTask (ConversionTask):
    """Dataclass that serves as a container for task data in automatic conversions"""

    folder_path: str
    mode = "auto"

    def __str__(self):
        return f"{self.final_name} to be auto-converted from {self.folder_path}"

    def __format__(self, format_spec):
        return f"{str(self):{format_spec}}"

@dataclass
class ManualConversionTask (ConversionTask):
    """Dataclass that serves as a container for building custom and manual tasks"""

    destination_folder:str
    files: list[str] #List to save img's paths
    mode = "manual"

    def __str__(self):
        if self.mode == "manual":
            return f"{self.final_name} to be converted to {self.destination_folder}"
        else:
            return f"{self.final_name} to be merged on {self.destination_folder}"

    def __format__(self, format_spec):
        return f"{str(self):{format_spec}}" 

class TaskManager:
    """Class that manages the logic for conversions, using utility functions from utils"""

    task_queue:list[ConversionTask] = []
    
    def show_queue(self):
        """Getter method to see the task queue"""

        return self.task_queue

    def create_auto_task(self, path_to_folder:str, name:str = ""):
        """Method to create tasks for the queue"""

        if not os.path.exists(path_to_folder) or not os.path.isdir(path_to_folder):
            raise FileNotFoundError("The given path is not valid")
        
        if name == "":
            name = path_to_folder.split("/")[-1] + ".pdf"
        elif not name.endswith(".pdf"):
            name = name + ".pdf"
        
        task = AutoConversionTask(name, "auto", path_to_folder)

        self.task_queue.append(task)
        return task
    
    def add_other_task(self, task:ConversionTask):
        """Generic method to add miscellaneuos tasks that 
        are built outside the ConversionManager"""

        if isinstance(task, ConversionTask) and\
            task not in self.task_queue:

            self.task_queue.append(task)
    
    def __convert_pdf__(self, final_name:str, imgs:list[str], dest_path:str):
        """Method that wraps the conversion to pdf"""

        f_name = os.path.join(dest_path, final_name)

        if os.path.exists(f_name):
            pass

        with open(f_name, "wb") as final_pdf:
            final_pdf.write(img2pdf.convert(imgs))

    def __autoconvert__(self, task:AutoConversionTask):
        """Method to manage the automatic conversion tasks"""

        imgs = utils.extract_imgs(task.folder_path)
        self.__convert_pdf__(task.final_name, imgs, task.folder_path)
    
    def __manualconvert__(self, task:ManualConversionTask):
        """Method to manage the manual conversion tasks""" 

        imgs = self.__convert_list__(task)

        self.__convert_pdf__(task.final_name, imgs, task.destination_folder)
    
    def __merge__(self, task:ManualConversionTask):
        """Method to merge pdf files"""

        f_name = os.path.join(task.destination_folder, task.final_name)

        with PdfWriter(f_name) as final_pdf:

            for pdf in task.files:
                with PdfReader(pdf) as current:

                    final_pdf.append(current)
            
            final_pdf.write(f_name)
    
    def __convert_list__(self, task:ManualConversionTask):
        """Method to convert the .webp images when conversion starts"""

        imgs = task.files
        final_imgs = []

        for img in imgs:
            name = os.path.basename(img)

            if name.endswith(".webp"):
                img = utils.convert_webp(img, name, os.path.dirname(img))
            
            final_imgs.append(img)
        
        return final_imgs
            
    def process_first(self) -> bool:
        """Method to perform the first of all the queued task
        Alternative for generator (that shit broke my app for some reason)"""

        task:ConversionTask

        if len(self.task_queue) > 0:
            task = self.task_queue.pop(0)

            if task.mode == "auto":
                self.__autoconvert__(task)
                return True
            
            elif task.mode == "merge":
                self.__merge__(task)
                return True
            
            elif task.mode == "manual":
                self.__manualconvert__(task)
                return True
        
        return False


        
    
    def remove_from_queue(self, value:ConversionTask):
        """Method to remove from the task_queue"""

        if value in self.task_queue:
            self.task_queue.remove(value)