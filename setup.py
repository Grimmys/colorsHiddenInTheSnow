import os
import sys

from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Users\Grimmys\AppData\Local\Programs\Python\Python37\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Grimmys\AppData\Local\Programs\Python\Python37\tcl\tk8.6'

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Colors hidden in the Snow",
    options={"build_exe": {
        "packages": ["wasabi2d", "glcontext", "pygame", "moderngl"],
        "excludes": ["tkinter", "matplotlib"],
        "include_files": ["CREDITS", "images", "music", "fonts", "src"]
    }
    },
    version="0.0.1",
    executables=[Executable("main.py", base=base, targetName="Colors hidden in the Snow")]
)
