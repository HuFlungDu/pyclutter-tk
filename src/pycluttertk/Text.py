import clutter
import pango
import Widget

class Label(Widget.TextWidget,clutter.Text):
    

    _oldsettext = clutter.Text.set_text
    def set_text(self,text):
        self._oldsettext(text)

        

    def __init__(self,text=""):
        Widget.TextWidget.__init__(self)
        clutter.Text.__init__(self)

        
        self.set_editable(False)
        self.set_line_wrap(False)
        self.set_text(text)

        
    def set_alignment(self,alignment):
        if alignment == "left":
            self.set_line_alignment(pango.ALIGN_LEFT)
        elif alignment == "right":
            self.set_line_alignment(pango.ALIGN_RIGHT)
        elif alignment == "center":
            self.set_line_alignment(pango.ALIGN_CENTER)
