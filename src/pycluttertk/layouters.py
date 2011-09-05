import clutter
import gobject
import Widget
class _Box(Widget.GroupWidget,clutter.Box):
    __gsignals__ = {
                'clicked' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'released' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'enter' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'leave' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'motion' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'resized' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)) #@UndefinedVariable
        }
    def releaseall(self,stage,event):
        for i in self.get_children():
            i.releaseall(stage,event)
    
    def __init__(self,easingduration=0,easingmode=None,homogeneous=False,
                 packstart=0,spacing=0,useanimations=False):
        Widget.GroupWidget.__init__(self)
        layout = clutter.BoxLayout()
        layout.set_easing_duration(easingduration)
        if easingmode:
            layout.set_easing_mode(easingmode)
        layout.set_homogeneous(homogeneous)
        layout.set_pack_start(packstart)
        layout.set_spacing(spacing)
        layout.set_use_animations(useanimations)
        clutter.Box.__init__(self,layout)
        self.set_width(0)
        self.set_height(0)
        self.layout = layout
        
    

class VBox(_Box):
    __gtype_name__ = 'VBox'
    def pack(self,widget,expand,xfill,yfill,x_align,y_align):
        self.set_width(max(widget.get_width(), self.get_width()))
        self.layout.pack(widget,expand,xfill,yfill,x_align,y_align)
        height = 0
        width = 0
        for child in self.get_children():
            height += child.get_height()
            width = max(width,child.get_width())
        self.set_width(width)
        self.set_height(height)
        print self.get_height()
            
    def __init__(self,easingduration=0,easingmode=None,homogeneous=False,
                 packstart=0,spacing=0,useanimations=False):
        _Box.__init__(self,easingduration,easingmode,homogeneous,
                      packstart,spacing,useanimations)
        self.layout.set_vertical(True)
    
        
        
        
class HBox(_Box):
    __gtype_name__ = 'HBox'
    def pack(self,widget,expand,xfill,yfill,x_align,y_align):
        self.set_height(max(widget.get_height(), self.get_height()))
        self.layout.pack(widget,expand,xfill,yfill,x_align,y_align)
        height = 0
        width = 0
        for child in self.get_children():
            width += child.get_width()
            height = max(height,child.get_height())
        self.set_width(width)
        self.set_height(height)
    def __init__(self,easingduration=0,easingmode=None,homogeneous=False,
                 packstart=0,spacing=0,useanimations=False):
        _Box.__init__(self,easingduration,easingmode,homogeneous,
                      packstart,spacing,useanimations)
        self.layout.set_vertical(False)
