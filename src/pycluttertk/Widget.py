import clutter
import os
import gobject
class Widget():
    if os.name != "posix":
        from win32com.shell import shellcon, shell            
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
    _oldsetx = clutter.Actor.set_x
    def set_x(self,x):
        self.realx = x
        if self.get_stage() is None:
            self._oldsetx(x)
        else:
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsetx(self.realx*(float(stage.get_width())/resolution[0]))
    _oldgetx = clutter.Actor.get_x
    def get_x(self):
        return self.realx
    _oldsety = clutter.Actor.set_y
    def set_y(self,y):
        self.realy = y
        if self.get_stage() is None:
            self._oldsety(y)
        else:
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsety(self.realy*(float(stage.get_height())/resolution[1]))
        
    _oldgety = clutter.Actor.get_y
    def get_y(self):
        return self.realy
    _oldsetwidth = clutter.Actor.set_width
    def set_width(self,w):
        if w >= self.get_size_request()[0]:
            self.w = w
            if self.get_stage() is None:
                self._oldsetwidth(w)
            else:
                stage = self.get_stage()
                resolution = stage.get_resolution()
                self._oldsetwidth(self.w*(float(stage.get_width())/resolution[0]))
        else:
            self.set_width(self.get_size_request()[0])
        try:
            self.emit('resized', self)
        except:
            pass
    _oldgetwidth = clutter.Actor.get_width
    def get_width(self):
        return self.w
    _oldsetheight = clutter.Actor.set_height
    def set_height(self,h):
        if h >= self.get_size_request()[1]:
            self.h = h
            if self.get_stage() is None:
                self._oldsety(h)
            else:
                stage = self.get_stage()
                resolution = stage.get_resolution()
                self._oldsetheight(self.h*(float(stage.get_height())/resolution[1]))
        else:
            self.set_height(self.get_size_request()[1])
        try:
            self.emit('resized', self)
        except:
            pass
    _oldgetheight = clutter.Actor.get_height
    def get_height(self):
        return self.h
class PictureWidget(Widget):
    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_height(int(self.h*(float(stage.get_height())/resolution[1])))
        self.set_width(int(self.w*(float(stage.get_width())/resolution[0])))
    
class GroupWidget(Widget):
    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_x(self.realx)
        self.set_y(self.realy)
        self.set_height(self.h)
        self.set_width(self.w)
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
