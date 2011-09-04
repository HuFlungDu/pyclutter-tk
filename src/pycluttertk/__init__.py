import os
import platform
import shutil
import __main__


if os.name != "posix":
    #Need to make eclipse shut up already
    from win32com.shell import shellcon, shell            #@UnresolvedImport
    homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    pass
else:
    homedir = os.path.expanduser("~")
if not os.path.isdir(homedir+"/.pyclutter-tk"):
    os.mkdir(homedir+"/.pyclutter-tk")
if not os.path.isdir(homedir+"/.pyclutter-tk"+"/Themes"):
    libdir = os.path.dirname(os.path.abspath(
                getattr(__main__,'__file__','__main__.py')))
    shutil.copytree(libdir+"/Themes",homedir+"/.pyclutter-tk"+"/Themes")
    
_resolution = (0,0)
_stage = None

from Button import ImageButton, LabelButton
from GUI import GUI
from layouters import HBox, VBox
from menu import *
from Text import Label
from Texture import CairoTexture, Texture
from Window import Window
import Errors
