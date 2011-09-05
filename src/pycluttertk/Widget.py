import clutter
import os
import pycluttertk
from pycluttertk import Errors
class Widget(object):
    
    def __init__(self):
        if pycluttertk._stage is None:
            raise Errors.CreationError("Can't create widgets until a GUI context has been created")
    
    if os.name != "posix":
        #Need to make eclipse shut up already
        from win32com.shell import shellcon, shell            #@UnresolvedImport
        homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
    else:
        homedir = os.path.expanduser("~")
    appdatadir = homedir+"/.pyclutter-tk"
    _requestedwidth = 0
    _requestedheight = 0
    def request_size(self,width,height):
        self._requestedwidth = width
        self._requestedheight = height
    def get_size_request(self):
        return (self._requestedwidth,self._requestedheight)
    
    _oldsetwidth = clutter.Actor.set_width
    def set_width(self,w):
        self._oldsetwidth(w)
        self.emit('resized', self)
    _oldsetheight = clutter.Actor.set_height
    def set_height(self,h):
        self._oldsetheight(h)
        self.emit('resized', self)
    
class TextWidget(Widget):
    def __init__(self):
        Widget.__init__(self)
    def reallocate(self,stage,actorbox,flags):
        pass

class PictureWidget(Widget):
    def __init__(self):
        Widget.__init__(self)
    def reallocate(self,stage,actorbox,flags):
        self.set_height(int(self._height*(float(pycluttertk._stage.get_height())/pycluttertk._resolution[1])))
        self.set_width(int(self._width*(float(pycluttertk._stage.get_width())/pycluttertk._resolution[0])))
    
class GroupWidget(Widget):
    def __init__(self):
        Widget.__init__(self)
    def reallocate(self,stage,actorbox,flags):
        self.set_x(self._realx)
        self.set_y(self._realy)
        self.set_height(self._height)
        self.set_width(self._width)
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
