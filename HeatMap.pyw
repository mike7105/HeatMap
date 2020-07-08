# -*- coding: utf-8 -*-
"""HeatMap start"""
__version__ = 'Version:1.8'

import tkinter as tk
import tkinter.messagebox as msgbox
from modules.application import Application, resource_path
import logging
import os
import sys

# logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',
#                     filename=os.path.abspath('log.txt'))

ROOT = tk.Tk()
try:
    APP = Application(master=ROOT, version=__version__)
    ROOT.iconbitmap(resource_path(r"modules\ico\map_512x512_35976.ico"))
    ROOT.wm_state('zoomed')
    ROOT.mainloop()
except Exception as e:
    print("Unexpected error:", e)
    # msgbox.showinfo("Unexpected error:", e, parent=ROOT)
    msgbox.showinfo("Unexpected error:", sys.exc_info(), parent=ROOT)
finally:
    sys.exit()
