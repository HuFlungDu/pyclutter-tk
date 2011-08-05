import clutter
import pango

class Label(clutter.Text):
    _oldsetx = clutter.Text.set_x
    def set_x(self,x):
        if self.get_stage() is None:
            self._oldsetx(x)
        else:
            self.realx = x
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsetx(self.realx*(float(stage.get_width())/resolution[0]))
    _oldgetx = clutter.Text.get_x
    def get_x(self):
        return self.realx
    _oldsety = clutter.Text.set_y
    def set_y(self,y):
        if self.get_stage() is None:
            self._oldsety(y)
        else:
            self.realy = y
            stage = self.get_stage()
            resolution = stage.get_resolution()
            self._oldsety(self.realy*(float(stage.get_height())/resolution[1]))
        
    _oldgety = clutter.Text.get_y
    def get_y(self):
        return self.realy

    _oldsettext = clutter.Text.set_text
    def set_text(self,text):
        self._oldsettext(text)
        self.h = self.get_height()
        self.w = self.get_width()
        
    
    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_scale((float(stage.get_width())/resolution[0]),
                       (float(stage.get_height())/resolution[1]))
    def __init__(self):
        
        clutter.Text.__init__(self)
        self.set_editable(False)
        self.set_line_wrap(False)
        
        self.h = self.get_height()
        self.w = self.get_width()
        self.realx = self._oldgetx()
        self.realy = self._oldgety()
    def set_alignment(self,alignment):
        if alignment == "left":
            self.set_line_alignment(pango.ALIGN_LEFT)
        elif alignment == "right":
            self.set_line_alignment(pango.ALIGN_RIGHT)
        elif alignment == "center":
            self.set_line_alignment(pango.ALIGN_CENTER)
