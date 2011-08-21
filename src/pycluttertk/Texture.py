import clutter
import Widget

class Texture(Widget.PictureWidget,clutter.Texture):   
    def releaseall(self,stage,event):
        pass
    def __init__(self,filename=None, disable_slicing=False, load_async=False, load_data_async=False):
        clutter.Texture.__init__(self,filename,disable_slicing,load_async,load_data_async)
        self.w = self.get_width()
        self.h = self.get_height()
class CairoTexture(Widget.PictureWidget,clutter.CairoTexture): 
    def releaseall(self,stage,event):
        pass
    def __init__(self,width,height):
        self.set_height(height)
        self.set_width(width)
        clutter.CairoTexture.__init__(self,self.get_width(),self.get_height())
