"""Script that contains all the builders for each task"""

import os
from . import utils
from .conversion import AutoConversionTask, ManualConversionTask
from pathvalidate import sanitize_filename, sanitize_filepath, is_valid_filename, is_valid_filepath

class NonReadyTaskException(BaseException):
    """Exception that represents when a task doesn't have the required data"""

class ManualTaskBuilder:
    """Task to build the task without having real access to them"""

    task: ManualConversionTask

    def __init__(self):

        self.task = ManualConversionTask(None, "manual", None, [])
    
    def get_task(self):
        """Method that returns a built instance of ManualConversionTask
        Throws NonReadyTaskException if the required task doesn't have
        all the required data to work"""

        if self.task.files == []:
            raise NonReadyTaskException("There's no images selected to convert")

        if not self.__ispathvalid__():
            raise NonReadyTaskException("Invalid path or no path provided")

        return self.task
    
    def add_file(self, file:str):
        """Adds a single image to the task"""

        if not os.path.exists(file):
            raise AttributeError("The given path doesn'exists")
        
        if not (file.endswith(".jpg") or file.endswith(".jpeg")\
                or file.endswith(".png") or file.endswith("webp")):
            
            raise AttributeError("The given file is not a valid image file")

        self.__append_file__(file)

    def __ispathvalid__(self):
        """Little flag method to validate name and folder"""

        if self.task.final_name is None or self.task.destination_folder is None:
            return False

        name = self.__get_final_name__()
        folder = self.__get_dest_fold__()

        if not os.path.exists(folder):
            return False
    
        if not os.path.isdir(folder):
            return False
        
        if not name.endswith(".pdf"):
            return False

        path = os.path.join(folder, name)

        if os.path.exists(path):
            return False

        return True

    def set_final_name(self, new_name:str):
        """Setter method for final name"""

        name_s = sanitize_filename(new_name)

        if not name_s.endswith(".pdf"):
            name_s = name_s + ".pdf"

        self.task.final_name = name_s

    def set_destination_folder(self, new_path:str):
        """Setter method for destination folder"""

        self.task.destination_folder = new_path
    
    def __get_final_name__(self):
        """Getter method for task final name"""

        return self.task.final_name
    
    def __get_dest_fold__(self):
        """Getter method for task destination folder"""

        return self.task.destination_folder
    
    def __append_file__(self, file:str):
        """Append shortening method"""

        self.task.files.append(file)
    
    def get_files(self):
        """Getter method for imgs in task"""

        return self.task.files


class MergeTaskBuilder(ManualTaskBuilder):
    """Builder class for MergeConversionTasks"""

    def __init__(self):

        self.task = ManualConversionTask(None, "merge", None, [])

    

    #Override
    def add_file(self, file:str):
        """Method to add pdf files to the merge task"""

        if not os.path.exists(file):
            raise AttributeError("The given file doesn't exists")
        
        if not file.endswith(".pdf"):
            raise AttributeError("The given file is not a pdf file")
        
        self.__append_file__(file)
    
    #Override
    def get_task(self) -> ManualConversionTask:
        """Method to get a full merge task"""

        if not self.__ispathvalid__():
            raise NonReadyTaskException("The given filename is not valid")

        t_n = 0
        for a in self.get_files():
            t_n += 1
        
        if t_n <= 1:
            raise NonReadyTaskException("You cannot merge one or zero documents")

        return self.task


class AutoTaskBuilder:
    pass