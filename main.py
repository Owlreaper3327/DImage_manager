"""Simple console script to convert images into pdf"""
#First, we define our imports
import os
import img2pdf
from PIL import Image

#Here we'll declare constants


objdir = "" #variable for image's dir path
final_name = "" #defines the final name of the resultant pdf
imgs = [] #Stores the images in dir
queue = [] #queue of paths
progress = 0 #progress
com = "" #stores the command to execute
COMMANDS = {}


#Here we'll define functions

def convert_webp(img, name):
    """Due a significant compatibility problem with .webp images, I added this funny method"""

    if not os.path.exists("temp/"):
        os.mkdir("temp")


    image = Image.open(img).convert("RGB")
    ruta_relativa = os.path.join("temp/", name.split(".")[0] + ".jpg")
    ruta_abs = os.path.abspath(ruta_relativa)
    image.save(ruta_abs, "jpeg")
    return ruta_abs

def extract_imgs(path_to):
    """This function will perform a search in the dir you pass in the params and retrun the images"""
    
    imgs = []
    
    for piname in os.listdir(path_to):
        #For compatibility reasons, this code only accepts 4 formats
        if not (piname.endswith(".jpg") or piname.endswith(".png") or piname.endswith(".jpeg") or piname.endswith(".webp")):
            continue
        
        path = os.path.join(path_to, piname)

        if os.path.isdir(path):
            continue
        
        if (piname.endswith(".webp")):
            path = convert_webp(path, piname)

        imgs.append(path)
    
    imgs.sort()
    
    return imgs

def convert_pdf(path_to, final_name, imgs):
    """This function will perform the pdf conversion and give a decent name"""

    name_f = final_name + ".pdf"

    path = os.path.join(path_to, name_f)

    cont = 0

    with open(path, "wb") as final_pdf:
        final_pdf.write(img2pdf.convert(imgs))

    print("\a")
    clean()


def clean():
    """Cleans conversion cache"""
    for cache_im in os.listdir("temp/"):
        path = os.path.join(os.path.abspath("temp/"), cache_im)
        os.remove(path)


def extract_queue():
    """Given the default path, this will extract all the folders to convert and put them in the queue"""
    
    path = ""

    try:
        with open("save.txt", "r") as sav:
            path = sav.readline()

    except Exception:
        print("Unreadable sav file or there's no default path setted")
        print("Aborting operation...")
        return
    else:
        for fi_name in os.listdir(path):
            path_2 = os.path.join(path, fi_name)

            if not os.path.isdir(path_2):
                continue

            queue.append((fi_name, path_2))
    
    return

#Currently in construction
def convert_pdf_progressive(path_to, final_name, imgs:list[str]):
    """This function will convert the imgs into pdf one to one, to give a propper feedback
    of conversion progress"""

    name_f = final_name + ".pdf"

    path = os.path.join(path_to, name_f)

    cont = 0
    total = len(imgs)

    with open(path, "ab") as final_pdf:

        for img in imgs:

            per = (cont/total) * 100
            print(f"Current conversion progress {per:.2f}%")

            new_img = img
            if img.endswith("webp"):
                name = img.split("/")[-1]
                name = name.split(".")[0]
                new_img = convert_webp(img, name)

            final_pdf.write(img2pdf.convert(new_img))
            clean()
            cont += 1

    return

def complete_conversion():
    """This script will execute the conversion for an already done queue"""
    progress = 0
    for name, dir in queue:
        imgs = extract_imgs(dir)
        convert_pdf(dir, name, imgs)
        print("\a")
        progress += 1
        print(f"Actual progress {progress}/{len(queue)}")
        print(f"{(progress/len(queue)) * 100:.2f}% completed")
    
    print("\a")
    print("\a")
    print("FINISHED!")
    return


def main_path():

    while(True):
        try:
            objdir = input("Introduce the complete path to your pictures folder: ")

            if not (os.path.exists(objdir)):
                raise OSError("Path included doesn't exist")

            if not (os.path.isdir(objdir)):
                raise OSError("Wrong input, must be a folder")
            
            final_name = input("Introduce the name to your resultant file: ")
            
            if final_name == "?def" or final_name == "":
                final_name = objdir.split("/")[-1]

            queue.append((final_name, objdir))

        except OSError:
            print("Path you included is not valid")
            continue
        else:
            val = input("Do you want to add more files? (s/n)\n")

            if val.lower() == "s":
                continue
            else:
                break
    
    complete_conversion()
    return

def take_default_path():
    """This is for establishing the default path for conversion"""
    """With this option, app will save the path in a txt (later i'll do a propper savefile)"""
    """Later, will use this path to convert all the directories there into pdf files"""

    try:
        with open("save.txt", "r") as sav:
            objdir = sav.readline()

    except OSError:
        print("Save file not found. Create one? (y/n)")
        c = input()

        if c.lower == "y":
            set_default_path()
        else:
            return
    else:
        extract_queue()
        complete_conversion()
    
    return


def set_default_path():
    """This will set the default path to recursive conversion"""

    path = input("Introduce the full path to your conversion site: ")

    while(True):
        if not os.path.exists(path):
            print("The introduced path it's no valid")
            continue
            
        if not os.path.isdir(path):
            print("The introduced path must be a directory")
            continue

        with open("save.txt", "w") as sav:
            sav.write(path)
            break
    
    return
    
def display_guide():
    """This function will show available commands to execute"""

    print("Welcome to the Owl's simple pdf converter\nWhat do you want today?")

    print("List of commands:\n")
    print("?def to go on and convert default route")
    print("?cdef to change default route")
    print("?exit to end")
    print("")

    print("Or simply press enter to convert one to one")


#Here we'll define the main logic of the program

COMMANDS = {"" : main_path, "?def":take_default_path, "?cdef":set_default_path}

while(True):

    objdir = "" #variable for image's dir path
    final_name = "" #defines the final name of the resultant pdf
    imgs = [] #Stores the images in dir
    queue = [] #queue of paths
    progress = 0 #progress
    com = ""

    display_guide()
    com = input("Introduce your command: ")

    if not com in COMMANDS.keys():
        print("The provided word is not a command")
        continue
    else:
        COMMANDS[com]()