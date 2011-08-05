import clutter

class Texture(clutter.Texture):
    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_height(int(self.h*(float(stage.get_height())/resolution[1])))
        self.set_width(int(self.w*(float(stage.get_width())/resolution[0])))

    def __init__(self,filename=None, disable_slicing=False, load_async=False, load_data_async=False):
        clutter.Texture.__init__(self,filename,disable_slicing,load_async,load_data_async)
        self.w = self.get_width()
        self.h = self.get_height()
class CairoTexture(clutter.CairoTexture):
    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_height(int(self.h*(float(stage.get_height())/resolution[1])))
        self.set_width(int(self.w*(float(stage.get_width())/resolution[0])))
        
    def releaseall(self,stage,event):
        pass
    def __init__(self,width,height):
        clutter.CairoTexture.__init__(self,width,height)
        self.w = self.get_width()
        self.h = self.get_height()
