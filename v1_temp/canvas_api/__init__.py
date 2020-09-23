print(" ██╗   ██╗██████╗  ██████╗")
print(" ██║   ██║██╔══██╗██╔════╝")
print(" ██║   ██║██████╔╝██║     ")
print(" ██║   ██║██╔══██╗██║     ")
print(" ╚██████╔╝██████╔╝╚██████╗")
print("  ╚═════╝ ╚═════╝  ╚═════╝")

import logging
from logging.config import fileConfig

# load the logging configuration
fileConfig('logging.ini')

from canvas_api.util.api import CanvasInstance

canvas = CanvasInstance("canvas.cfg")
