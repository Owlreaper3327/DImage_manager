"""Little script to test the conversion features"""

import os
from converter.conversion import TaskManager, ConversionTask, ManualConversionTask,\
    AutoConversionTask
from converter.task_builders import ManualTaskBuilder, MergeTaskBuilder
from converter import utils

path = ""
name = ""
dest_route = "/home/frost/Descargas/Pruebas"

queue = TaskManager()

COMMANDS = {}

def create_merge(mode = "merge"):

    file = ""
    task = MergeTaskBuilder() if mode == "merge" else ManualTaskBuilder()
    task.set_destination_folder(dest_route)
    cont = 0

    while True:

        file = input("Introduzca la ruta a un archivo")

        try:
            task.add_file(file)
            cont += 1
        except AttributeError as e:
            print(e)
            continue

        e = input("Quiere añadir más archivos s/n: ")

        if e == "n":
            break

    while True:
        name = input("Añada un nombre válido terminado en pdf")

        try:
            task.set_final_name(name)
            break
        except AttributeError as e:
            print("Nombre no válido")
            continue

    task_b = task.get_task()

    queue.add_other_task(task_b)

def create_auto():

    while True:

        folder = input("Introduzca la ruta a una carpeta")

        try:
            queue.create_auto_task(folder)
            return
        except FileNotFoundError as e:
            continue

def create_manual():
    create_merge("manual")

def start():
    queue.process_queue()
    queue.task_queue.clear()


COMMANDS = {"ma": create_manual, "me": create_merge, "a": create_auto, "st": start}

while True:

    com = input("Introduzca un comando: ")

    if com not in COMMANDS.keys() and com != "exit":
        print("Comando no valido")
        continue

    if com == "exit":
        break
    else:
        COMMANDS[com]()

