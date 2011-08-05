import clutter
class GroupWidget():
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
    '''_oldsetwidth = clutter.Group.set_width
    def set_width(self,w):
        if self.get_stage() is None:
            self._oldsetwidth(w)
        else:
            self.w = w
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsetwidth(self.w*(float(stage.get_width())/resolution[0]))
    _oldgetwidth = clutter.Group.get_width
    def get_width(self):
        return self.w
    _oldsetheight = clutter.Group.set_height
    def set_height(self,h):
        if self.get_stage() is None:
            self._oldsety(h)
        else:
            self.h = h
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsetheight(self.h*(float(stage.get_height())/resolution[1]))
        
    _oldgetheight = clutter.Group.get_height
    def get_height(self):
        return self.h'''
