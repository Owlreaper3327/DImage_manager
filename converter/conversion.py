"""Script that contains the classes for conversion"""

import img2pdf
import os
from dataclasses import dataclass
from . import utils

@dataclass
class ConversionTask:
    """Dataclass that serves a a container for task data in conversions"""

    final_name: str
    folder_path: str

    def __str__(self):
        return f"{self.final_name} to be converted from {self.folder_path}"

    def __format__(self, format_spec):
        return f"{str(self):{format_spec}}"

class ConversionManager:
    """Class that manages the logic for conversions, using utility functions from utils"""

    task_queue: list[ConversionTask]

    def __init__(self, final_folder:str):
        """Constructor for the Class"""

        if not os.path.isdir(final_folder):
            self.destination_folder = os.path.abspath("")
        else:
            self.destination_folder = final_folder
    
    def show_queue(self):
        """Getter method to see the task queue"""

        return self.task_queue

    def create_task(self, path_to_folder:str, name:str = ""):
        """Method to create tasks for the queue"""

        if not os.path.exists(path_to_folder) or not os.path.isdir(path_to_folder):
            raise FileNotFoundError("The given path is not valid")
        
        if name == "":
            name = path_to_folder.split("/")[-1] + ".pdf"
        elif not name.endswith(".pdf"):
            name = name + ".pdf"
        
        task = ConversionTask(name, path_to_folder)

        self.task_queue.append(task)