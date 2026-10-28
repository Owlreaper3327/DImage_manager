"""Script that contains all the utility functions that doesn't need to be encapsulated"""

import os
from PIL import Image

def convert_webp(img_abspath:str, name:str, path_to_dir:str=None):
    """Utility method to handle the .webp images"""

    if path_to_dir is None:
        fol = os.path.dirname(img_abspath)

        path_to_dir = os.path.join("/temp/", fol)
        path_to_dir = os.path.abspath(path_to_dir)

    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)


    image = Image.open(img_abspath).convert("RGB")
    relative_path = os.path.join(path_to_dir, name.split(".")[0] + ".jpg")
    abs_path = os.path.abspath(relative_path)
    image.save(abs_path, "jpeg")
    return abs_path

def clean_cache(folder_path:str, clean_all:bool=False):
    """Utility method to clean conversion cache"""

    if not os.path.exists(folder_path):
        raise FileNotFoundError("The path introduced doesn't exists")
    
    if not os.path.isdir(folder_path):
        raise FileExistsError("The requested path is not a folder")
    
    for file in os.listdir(folder_path):

        if file.endswith("jpg") or (file.endswith(".webp") or file.endswith(".png") or\
                                     file.endswith(".jpeg") and clean_all):

            del_path = os.path.join(folder_path, file)
            os.remove(del_path)

def clean_temp():
    """Utility method to clean conversion cache on /temp"""

    temp = os.path.abspath("/temp")

    if os.path.exists(temp):

        for file in os.listdir(temp):

            ab_p = os.path.join(temp, file)

            if os.path.isdir(ab_p):
                clean_cache(ab_p, True)
            else:
                os.remove(ab_p)
        
        try:
            os.rmdir(temp)
        
        except OSError as e:
            pass
    

def extract_imgs(path_to:str):
    """Utility method to extract the images of a given folder"""

    imgs = []

    if not os.path.exists(path_to):
        raise FileNotFoundError("The path introduced doesn't exists")
    
    if not os.path.isdir(path_to):
        raise FileExistsError("The requested path is not a folder")
    
    for file in os.listdir(path_to):
        
        if file.endswith(".jpg") or file.endswith(".png")\
            or file.endswith(".jpeg") or file.endswith(".webp"):

            img = os.path.join(path_to, file)

            if file.endswith(".webp"):
                img = convert_webp(img, file, path_to)
            
            imgs.append(img)
    
    imgs.sort()
    return imgs

def extract_queue(dest_folder:str) -> list[str]:
    """Utility method to extract folders to create auto tasks"""

    if not os.path.exists(dest_folder):
        raise FileNotFoundError("The given path doesn't exists")

    if not os.path.isdir(dest_folder):
        raise FileNotFoundError("The given path doesn't leads to a folder")
    
    tasks = []
    
    for file in os.listdir(dest_folder):

        full = os.path.join(dest_folder, file)

        if os.path.isdir(full):
            tasks.append(full)
    
    return tasks