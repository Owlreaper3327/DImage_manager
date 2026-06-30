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
        return f"{self.final_name} to be converted from {self.folder_path}"

    def __format__(self, format_spec):
        return f"{str(self):{format_spec}}"

@dataclass
class ManualConversionTask (ConversionTask):
    """Dataclass that serves as a container for building custom and manual tasks"""

    destination_folder:str
    imgs: list[str] #List to save img's paths
    mode = "manual"

@dataclass
class MergeConversionTask(ConversionTask):
    """Dataclass that serves as a container to manage the merge tasks"""

    destination_folder:str
    merges:list[str]
    mode = "merge"

class TaskManager:
    """Class that manages the logic for conversions, using utility functions from utils"""

    task_queue = []

    def __init__(self, final_folder:str):
        """Constructor for the Class"""

        if not os.path.isdir(final_folder):
            self.destination_folder = os.path.abspath("")
        else:
            self.destination_folder = final_folder
    
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
    
    def add_other_task(self, task:ConversionTask):
        """Generic method to add miscellaneuos tasks that 
        are built outside the ConversionManager"""

        if isinstance(task, ConversionTask):
            self.task_queue.append(task)
    
    def __convert_pdf__(self, final_name:str, imgs:list[str], dest_path:str):
        """Method that wraps the conversion to pdf"""

        f_name = os.path.join(dest_path, final_name)

        with open(f_name, "wb") as final_pdf:
            final_pdf.write(img2pdf.convert(imgs))

    def __autoconvert__(self, task:AutoConversionTask):
        """Method to manage the automatic conversion tasks"""

        imgs = utils.extract_imgs(task.folder_path)
        self.__convert_pdf__(task.final_name, imgs, task.folder_path)
    
    def __manualconvert__(self, task:ManualConversionTask):
        """Method to manage the manual conversion tasks"""

        self.__convert_pdf__(task.final_name, task.imgs, task.destination_folder)
    
    def __merge__(self, task:MergeConversionTask):
        """Method to merge pdf files"""

        f_name = os.path.join(task.destination_folder, task.final_name)

        with PdfWriter(f_name) as final_pdf:

            for pdf in task.merges:
                with PdfReader(pdf) as current:

                    final_pdf.append(current)
        
    
    def process_queue(self):
        """Method to perform all the queued tasks"""

        for task in self.task_queue:

            match(task.mode is str):

                case "auto":
                    self.__autoconvert__(task)
                    break

                case "manual":
                    self.__manualconvert__(task)
                    break
                
                case "merge":
                    self.__merge__(task)
                    break