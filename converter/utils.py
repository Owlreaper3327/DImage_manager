"""Script that contains all the utility functions that doesn't need to be encapsulated"""

import os
from PIL import Image

def convert_webp(img_abspath:str, name:str, path_to_dir:str):
    """Utility method to handle the .webp images"""

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

        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")\
            or (file.endswith("webp") and clean_all):

            del_path = os.path.join(folder_path, file)
            os.remove(del_path)

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