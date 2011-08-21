import clutter
import gobject
import Widget
class _Box(Widget.GroupWidget,clutter.Box):
    def releaseall(self,stage,event):
        for i in self.get_children():
            i.releaseall(stage,event)
    
    def __init__(self,easingduration=0,easingmode=None,homogeneous=False,
                 packstart=0,spacing=0,useanimations=False):
        layout = clutter.BoxLayout()
        layout.set_easing_duration(easingduration)
        if easingmode:
            layout.set_easing_mode(easingmode)
        layout.set_homogeneous(homogeneous)
        layout.set_pack_start(packstart)
        layout.set_spacing(spacing)
        layout.set_use_animations(useanimations)
        self.layout = layout
        clutter.Box.__init__(self,layout)
    

class VBox(_Box):
    def pack(self,widget,expand,xfill,yfill,x_align,y_align):
        self.set_width(max(widget.get_width(), self.get_width()))
        if self.get_stage() != None:
            widget.stage = self.get_stage()
            widget.resolution = widget.stage.get_resolution()
        self.layout.pack(widget,expand,xfill,yfill,x_align,y_align)
    def __init__(self,easingduration=0,easingmode=None,homogeneous=False,
                 packstart=0,spacing=0,useanimations=False):
        _Box.__init__(self,easingduration,easingmode,homogeneous,
                      packstart,spacing,useanimations)
        self.layout.set_vertical(True)
    
        
        
        
class HBox(_Box):
    def pack(self,widget,expand,xfill,yfill,x_align,y_align):
        self.set_height(max(widget.get_height(), self.get_height()))
        self.layout.pack(widget,expand,xfill,yfill,x_align,y_align)
    def __init__(self,easingduration=0,easingmode=None,homogeneous=False,
                 packstart=0,spacing=0,useanimations=False):
        _Box.__init__(self,easingduration,easingmode,homogeneous,
                      packstart,spacing,useanimations)
        self.layout.set_vertical(False)
