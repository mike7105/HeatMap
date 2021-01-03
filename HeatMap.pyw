# -*- coding: utf-8 -*-
"""HeatMap start"""
__version__ = 'Version:1.9'

import tkinter as tk
import tkinter.messagebox as msgbox
import traceback
from modules.application import Application, resource_path
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
    trace_inf = traceback.format_exc()
    print(e)
    print("Unexpected error:", trace_inf)
    msgbox.showinfo("Unexpected error:", trace_inf)
    ROOT.destroy()
finally:
    sys.exit()
