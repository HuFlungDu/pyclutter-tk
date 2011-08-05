import clutter
import cairo
import gobject
from xml.etree import ElementTree as ET
import Texture
import Text

class ImageButton(clutter.Group):
    __gtype_name__ = 'ImageButton'
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

    def __init__(self,theme,width,height):
        self.w = width
        self.h = height
        self.pressed = False
        clutter.Group.__init__(self)
        self.realx = self._oldgetx()
        self.realy = self._oldgety()
        self.theme = theme
        self.themepath=("Themes/" + theme)
        guixmlfile = open(self.themepath + "/GUI.xml")
        guixml = ET.XML(guixmlfile.read())
        self.buttonxml = guixml.find("button")
        self.outxml = self.buttonxml.find("out")
        self.inxml = self.buttonxml.find("in")
        self.hoverxml = self.buttonxml.find("hover")
        
        self._in = self.makestate("in")
        self._out = self.makestate("out")
        self._hover = self.makestate("hover")
        self.add(self._in)
        self.add(self._out)
        self.add(self._hover)
        self._out.show()
        self._hover.hide()
        self._in.hide()
        self._textures = (self._out,
                            self._hover,
                            self._in)
        
        self.set_reactive(True)
        self.connect("button-press-event", self.clicked)
        self.connect("button-release-event", self.released)
        self.connect("enter-event", self.enter)
        self.connect("leave-event", self.leave)
        self.connect('motion-event',self.motion)
        
    def releaseall(self,stage,event):
        if self.pressed:
            self._out.show()
            self._hover.hide()
            self._in.hide()
            self.pressed = False
    def clicked(self,stage, event):
        if event.button==1:
            self._out.hide()
            self._hover.hide()
            self._in.show()
            self.pressed = True
            for i in [x for x in self.get_children() if not x in self._textures]:
                i.set_y(i.get_y()+1)
                i.set_x(i.get_x()+1)
        if self.get_stage() is not None:
            stage = self.get_stage()
            resolution = stage.get_resolution()
            event.y = event.y/(float(stage.get_height())/resolution[1])
            event.x = event.x/(float(stage.get_width())/resolution[0])
        self.emit("clicked",event)
    def released(self,stage,event):
        if self.pressed:
            if event.button==1:
                self._out.hide()
                self._hover.show()
                self._in.hide()
                self.pressed = False
                for i in [x for x in self.get_children() if not x in self._textures]:
                    i.set_y(i.get_y()-1)
                    i.set_x(i.get_x()-1)
            if self.get_stage() is not None:
                stage = self.get_stage()
                resolution = stage.get_resolution()
                event.y = event.y/(float(stage.get_height())/resolution[1])
                event.x = event.x/(float(stage.get_width())/resolution[0])
            self.emit("released",event)
    def enter(self,stage,event):
        if self.pressed:
            self._out.hide()
            self._hover.hide()
            self._in.show()
            for i in [x for x in self.get_children() if not x in self._textures]:
                i.set_y(i.get_y()+1)
                i.set_x(i.get_x()+1)
        else:
            self._out.hide()
            self._hover.show()
            self._in.hide()
        self.emit("enter",event)
    def leave(self,stage,event):
        self._out.show()
        self._hover.hide()
        self._in.hide()
        if self.pressed:
            for i in [x for x in self.get_children() if not x in self._textures]:
                i.set_y(i.get_y()-1)
                i.set_x(i.get_x()-1)
        self.emit("leave",event)
    def motion(self,stage,event):
        if self.get_stage() is not None:
            stage = self.get_stage()
            resolution = stage.get_resolution()
            event.y = event.y/(float(stage.get_height())/resolution[1])
            event.x = event.x/(float(stage.get_width())/resolution[0])
        self.emit("motion",event)  
    
    def makestate(self,state):
        
        if state == "out":
            xml = self.outxml
        elif state == "in":
            xml = self.inxml
        elif state == "hover":
            xml = self.hoverxml
        if xml.get("type") == "gradient":
            button=Texture.CairoTexture(int(self.w), int(self.h))
            context = button.cairo_create()
            context.scale(self.w, self.h)
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
            
            rounded = xml.find("rounded")
            r = float(rounded.get("topleft"))*.01
            context.move_to(r,0)                      # Move to A
            r = float(rounded.get("topright"))*.01
            context.line_to(1-r,0)                    # Straight line to B
            context.curve_to(1,0,1,0,1,r)       # Curve to C, Control points are both at Q1
            r = float(rounded.get("bottomright"))*.01
            context.line_to(1,1-r)                  # Move to D
            context.curve_to(1,1,1,1,1-r,1) # Curve to E
            r = float(rounded.get("bottomleft"))*.01
            context.line_to(r,1)                    # Line to F
            context.curve_to(0,1,0,1,0,1-r)       # Curve to G
            r = float(rounded.get("topleft"))*.01
            context.line_to(0,r)                      # Line to H
            context.curve_to(0,0,0,0,r,0)             # Curve to A
            #path = context.copy_path()
            context.fill()
            '''border = xml.find("border")
            color = border.get("color")
            color = [(int(color[i]+color[i+1],16)/float(0xFF)) for i in range(0,len(color),2)]
            #context.append_path(path)
            context.set_source_rgb(color[0],color[1],color[2])
            #context.set_line_width(.02)'''
            '''r = float(rounded.get("topleft"))*.01
            context.move_to(r,0)
            r = float(rounded.get("topright"))*.01
            context.line_to(1-r,0)
            context.curve_to(1,0,1,0,1,r)
            linewidth=float(border.get("top"))
            context.set_line_width(linewidth/self.h)
            context.stroke()
            context.move_to(1,r)
            r = float(rounded.get("bottomright"))*.01
            context.line_to(1,1-r)
            linewidth=float(border.get("right"))
            context.set_line_width(linewidth/self.w)
            context.stroke()
            context.move_to(1-r,1)
            r = float(rounded.get("bottomleft"))*.01
            context.line_to(r,1)
            linewidth=float(border.get("bottom"))
            context.set_line_width(linewidth/self.w)
            context.stroke()
            context.move_to(0,1-r)
            r = float(rounded.get("topleft"))*.01
            context.line_to(0,r)
            linewidth=float(border.get("left"))
            context.set_line_width(linewidth/self.w)
            context.stroke()'''
            del(context)
        elif xml.get("type") == "image":
            image=xml.find("image")
            imagepath=image.get("file")
            button=Texture.Texture(self.themepath+"/"+imagepath)
            button.set_width(self.w)
            button.set_height(self.h)
            
        return button


class LabelButton(ImageButton):
    __gtype_name__ = 'LabelButton'

    def reallocate(self,stage,actorbox,flags):
        resolution = stage.get_resolution()
        self.set_x(self.realx)
        self.set_y(self.realy)
        self.set_height(self.h*(float(stage.get_height())/resolution[1]))
        self.set_width(self.w*(float(stage.get_width())/resolution[0]))
        
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
        self.recenter()
    def recenter(self):
        self._text.set_x((self.w/2)-(self._text.get_width()/2))
        self._text.set_y((self.h/2)-(self._text.get_height()/2))
    
    def __init__(self,theme,label=" "):
        self.pressed = False
        clutter.Group.__init__(self)
        self.theme = theme
        self.themepath=("Themes/" + theme)
        guixmlfile = open(self.themepath + "/GUI.xml")
        self.realx = self._oldgetx()
        self.realy = self._oldgety()
        guixml = ET.XML(guixmlfile.read())
        buttonxml = guixml.find("button")
        self.outxml = buttonxml.find("out")
        self.inxml = buttonxml.find("in")
        self.hoverxml = buttonxml.find("hover")

        
        self._text = Text.Label()
        self._text.set_text(label)
        
        self.w = self._text.get_width()+(self._text.w/len(label)*2)
        self.h = self._text.get_height()*2
        
        self._in = self.makestate("in")
        self._out = self.makestate("out")
        self._hover = self.makestate("hover")
        self.add(self._in)
        self.add(self._out)
        self.add(self._hover)
        self.add(self._text)
        self.recenter()
        
        self._out.show()
        self._hover.hide()
        self._in.hide()
        self._text.show()
        self._textures = (self._out,
                            self._hover,
                            self._in)
        
        
        self.set_reactive(True)
        self.connect("button-press-event", self.clicked)
        self.connect("button-release-event", self.released)
        self.connect("enter-event", self.enter)
        self.connect("leave-event", self.leave)
        self.connect('motion-event',self.motion)
        #self.connect('allocation-changed',self.recenter)
