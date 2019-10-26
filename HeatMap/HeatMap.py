# -*- coding: utf-8 -*-
"""HeatMap start"""
__version__ = 'Version:1.6'
import sys
import tkinter as tk
import tkinter.messagebox as msgbox
from modules.application import Application


ROOT = tk.Tk()
try:
    APP = Application(master=ROOT, version=__version__)
    ROOT.wm_state('zoomed')
    ROOT.mainloop()
except:
    print("Unexpected error:", sys.exc_info()[0])    
    msgbox.showinfo("Unexpected error:", sys.exc_info()[0], parent=ROOT)
finally:
	input("Нажмите для выхода...")
