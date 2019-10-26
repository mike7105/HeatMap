# -*- coding: utf-8 -*-
"""HeatMap cx_Freeze компилляция проги"""
import os.path
from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
setup(
    name="HeatMap",
    version="1.6",
    description="HeatMap cxf",
    options={
        'build_exe': {
            'include_files':[
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                ],
            },
        },
    executables=[Executable("HeatMap.pyw")]
)
