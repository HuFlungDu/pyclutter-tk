import clutter
import pango
import Widget

class Label(Widget.GroupWidget,clutter.Text):
    

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
