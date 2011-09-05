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
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
    def __init__(self,window):
        clutter.Group.__init__(self)
        self.add(window)
        window.connect('allocation-changed',self.resizetowindow)
        self._realx = window.get_x()
        self._realy = window.get_y()
        self._height = window.get_height()
        self._width = window.get_width()
    def releaseall(self,stage,event):
        for i in self.get_children():
            i.releaseall(stage,event)
    def resizetowindow(self,stage,event,flags):
        pass
