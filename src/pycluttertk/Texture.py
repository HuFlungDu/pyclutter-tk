import clutter
import Widget
import gobject

class Texture(Widget.PictureWidget,clutter.Texture): 
    __gsignals__ = {
                    'resized' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)) #@UndefinedVariable
                    }  
    def releaseall(self,stage,event):
        pass
    def __init__(self,filename=None, disable_slicing=False, load_async=False, load_data_async=False):
        Widget.PictureWidget.__init__(self)
        clutter.Texture.__init__(self,filename,disable_slicing,load_async,load_data_async)
        self._width = self.get_width()
        self._height = self.get_height()
class CairoTexture(Widget.PictureWidget,clutter.CairoTexture): 
    __gsignals__ = {
                    'resized' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)) #@UndefinedVariable
                    }  
    def releaseall(self,stage,event):
        pass
    def __init__(self,width,height):
        Widget.PictureWidget.__init__(self)
        clutter.CairoTexture.__init__(self,width,height)
        self.set_height(height)
        self.set_width(width)
