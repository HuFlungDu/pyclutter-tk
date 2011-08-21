import clutter
import cairo

class WindowDoesNotExistError(Exception):
    pass
        

class WindowManager(object):
    _windows = []
    def __init__(self):
        pass
        
    def add_window(self,window):
        borderedwindow = BorderedWindow(window)
        self._windows.append(window)
        window.connect("kill",self.kill_window)
        return borderedwindow
    def kill_window(self,window):
        try:
            self._windows.remove(window)
        except:
            raise WindowDoesNotExistError(window.get_name())

class BorderedWindow(clutter.Group):
    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_x(self.realx)
        self.set_y(self.realy)
        self.set_height(self.h*(float(stage.get_height())/resolution[1]))
        self.set_width(self.w*(float(stage.get_width())/resolution[0]))
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
    _oldsetx = clutter.Group.set_x
    def set_x(self,x):
        if self.get_stage() is None:
            self._oldsetx(x)
        else:
            self.realx = x
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsetx(self.realx*(float(stage.get_width())/resolution[0]))
    _oldgetx = clutter.Group.get_x
    def get_x(self):
        return self.realx
    _oldsety = clutter.Group.set_y
    def set_y(self,y):
        if self.get_stage() is None:
            self._oldsety(y)
        else:
            self.realy = y
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsety(self.realy*(float(stage.get_height())/resolution[1]))
        
    _oldgety = clutter.Group.get_y
    def get_y(self):
        return self.realy
    def __init__(self,window):
        clutter.Group.__init__(self)
        self.add(window)
        window.connect('allocation-changed',self.resizetowindow)
        self.realx = window.get_x()
        self.realy = window.get_y()
        self.h = window.h
        self.w = window.w
    def releaseall(self,stage,event):
        for i in self.get_children():
            i.releaseall(stage,event)
    def resizetowindow(self,stage,event,flags):
        pass
