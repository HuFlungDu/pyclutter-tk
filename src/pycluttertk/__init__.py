import os
import platform
import shutil
import __main__
if os.name != "posix":
    from win32com.shell import shellcon, shell            
    homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
else:
    homedir = os.path.expanduser("~")
if not os.path.isdir(homedir+"/.pyclutter-tk"):
    os.mkdir(homedir+"/.pyclutter-tk")
if not os.path.isdir(homedir+"/.pyclutter-tk"+"/Themes"):
    libdir = os.path.dirname(os.path.abspath(
                getattr(__main__,'__file__','__main__.py')))
    shutil.copytree(libdir+"/Themes",homedir+"/.pyclutter-tk"+"/Themes")

from Button import *
from GUI import *
from layouters import *
from menu import *
from Text import *
from Texture import *
from Window import *
