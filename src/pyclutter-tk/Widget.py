import clutter
class GroupWidget():
    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_x(self.realx)
        self.set_y(self.realy)
        self.set_height(self.h)
        self.set_width(self.w)
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
    _oldsetx = clutter.Group.set_x
    def set_x(self,x):
        self.realx = x
        if self.get_stage() is None:
            self._oldsetx(x)
        else:
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsetx(self.realx*(float(stage.get_width())/resolution[0]))
    _oldgetx = clutter.Group.get_x
    def get_x(self):
        return self.realx
    _oldsety = clutter.Group.set_y
    def set_y(self,y):
        self.realy = y
        if self.get_stage() is None:
            self._oldsety(y)
        else:
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsety(self.realy*(float(stage.get_height())/resolution[1]))
        
    _oldgety = clutter.Group.get_y
    def get_y(self):
        return self.realy
    _oldsetwidth = clutter.Group.set_width
    def set_width(self,w):
        self.w = w
        if self.get_stage() is None:
            self._oldsetwidth(w)
        else:
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsetwidth(self.w*(float(stage.get_width())/resolution[0]))
    _oldgetwidth = clutter.Group.get_width
    def get_width(self):
        return self.w
    _oldsetheight = clutter.Group.set_height
    def set_height(self,h):
        self.h = h
        if self.get_stage() is None:
            self._oldsety(h)
        else:
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsetheight(self.h*(float(stage.get_height())/resolution[1]))
            print self,h
    _oldgetheight = clutter.Group.get_height
    def get_height(self):
        return self.h
