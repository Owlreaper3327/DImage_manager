"""This is the user interface for the program, that will use the logic from the main class
ConversionManager"""

import customtkinter
from converter.conversion import ConversionManager
from converter import utils
from converter.task_builders import ManualTaskBuilder, MergeTaskBuilder, AutoTaskBuilder, NonReadyTaskException
