import clutter
import cairo
import gobject
from xml.etree import ElementTree as ET
import Texture

class Window(clutter.Group):
    __gtype_name__ = 'Window'
    __gsignals__ = {
                'clicked' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
                'released' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
                'enter' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
                'leave' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
                'motion' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
        }
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

    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_x(self.realx)
        self.set_y(self.realy)
        self.set_height(self.h*(float(stage.get_height())/resolution[1]))
        self.set_width(self.w*(float(stage.get_width())/resolution[0]))
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
    def __init__(self,theme,name):
        clutter.Group.__init__(self)
        self.h=self.get_height()
        self.w=self.get_width()
        self.realx = self._oldgetx()
        self.realy = self._oldgety()
        self.theme = theme
        self.theme = theme
        self.themepath=("Themes/" + theme)
        guixmlfile = open(self.themepath + "/GUI.xml")
        self.realx = self._oldgetx()
        self.realy = self._oldgety()
        guixml = ET.XML(guixmlfile.read())
        windowxml = guixml.find("window")
        self.basexml = windowxml.find("base")
        self._windowtex=self.make()
        self.add(self._windowtex)
        
        self.set_reactive(True)
        self.connect("button-press-event", self.clicked)
        self.connect("button-release-event", self.released)
        self.connect("enter-event", self.enter)
        self.connect("leave-event", self.leave)
        self.connect('motion-event',self.motion)

    def releaseall(self,stage,event):
        for i in self.get_children():
            i.releaseall(stage,event)
    def clicked(self,stage, event):
        self.emit("clicked",event)
    def released(self,stage,event):
        self.emit("released",event)
    def enter(self,stage,event):
        self.emit("enter",event)
    def leave(self,stage,event):
        self.emit("leave",event)
    def motion(self,stage,event):
        self.emit("motion",event)
        
    def make(self):
        xml = self.basexml
        if xml.get("type") == "gradient":
            window=Texture.CairoTexture(10, 10)
            context = window.cairo_create()
            context.scale(10, 10)
            gradient = xml.find("gradient")
            
            if gradient.get("type") == "linear":
                start = gradient.get("start").split("-")
                end = gradient.get("end").split("-")
                pos1 = 0
                pos2 = 0
                pos3 = 0
                pos4 = 0
                if start[0] == "top":
                    pos2 = 0
                elif start[0] == "mid":
                    pos2 = .5
                elif start[0] == "bottom":
                    pos2 = 1
                if start[1] == "left":
                    pos1 = 0
                elif start[1] == "mid":
                    pos1 = .5
                elif start[1] == "right":
                    pos1 = 1
                if end[0] == "top":
                    pos4 = 0
                elif end[0] == "mid":
                    pos4 = .5
                elif end[0] == "bottom":
                    pos4 = 1
                if end[1] == "left":
                    pos3 = 0
                elif end[1] == "mid":
                    pos3 = .5
                elif end[1] == "right":
                    pos3 = 1
                color1 = gradient.get("color1")
                color2 = gradient.get("color2")
                color1 = [(int(color1[i]+color1[i+1],16)/float(0xFF)) for i in range(0,len(color1),2)]
                color2 = [(int(color2[i]+color2[i+1],16)/float(0xFF)) for i in range(0,len(color2),2)]
                pattern = cairo.LinearGradient(pos1, pos2, pos3, pos4)
                
                pattern.add_color_stop_rgb(0, color1[0], color1[1],color1[2])
                pattern.add_color_stop_rgb(1, color2[0], color2[1], color2[2])
                context.set_source(pattern)

            elif gradient.get("type") == "radial":
                start = gradient.get("start").split("-")
                end = gradient.get("end").split("-")
                pos1 = 0
                pos2 = 0
                pos3 = 0
                pos4 = 0
                if start[0] == "top":
                    pos2 = 0
                elif start[0] == "mid":
                    pos2 = .5
                elif start[0] == "bottom":
                    pos2 = 1
                if start[1] == "left":
                    pos1 = 0
                elif start[1] == "mid":
                    pos1 = .5
                elif start[1] == "right":
                    pos1 = 1
                if end[0] == "top":
                    pos4 = 0
                elif end[0] == "mid":
                    pos4 = .5
                elif end[0] == "bottom":
                    pos4 = 1
                if end[1] == "left":
                    pos3 = 0
                elif end[1] == "mid":
                    pos3 = .5
                elif end[1] == "right":
                    pos3 = 1
                color1 = gradient.get("color1")
                color2 = gradient.get("color2")
                color1 = [(int(color1[i]+color1[i+1],16)/float(0xFF)) for i in range(0,len(color1),2)]
                color2 = [(int(color2[i]+color2[i+1],16)/float(0xFF)) for i in range(0,len(color2),2)]
                radius1 = float(gradient.get("radius1"))*.01
                radius2 = float(gradient.get("radius2"))*.01
                pattern = cairo.RadialGradient(pos1, pos2, radius1, pos3, pos4, radius2)
                
                pattern.add_color_stop_rgb(0, color1[0], color1[1],color1[2])
                pattern.add_color_stop_rgb(1, color2[0], color2[1], color2[2])
                context.set_source(pattern)
            
            
            context.move_to(0,0)                    
            context.line_to(1,0)
            context.line_to(1,1)
            context.line_to(0,1)
            context.line_to(0,0)
            context.fill()
            del(context)
        elif xml.get("type") == "image":
            image=xml.find("image")
            imagepath=image.get("file")
            window=Texture.Texture(self.themepath+"/"+imagepath)
        return window
