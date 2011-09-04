import clutter
import gobject
from xml.etree import ElementTree as ET
import Texture
import Text
import Widget
import SharedFunctions
import pycluttertk

class ImageButton(Widget.GroupWidget,clutter.Group):
    __gtype_name__ = 'ImageButton'
    __gsignals__ = {
                'clicked' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'released' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'enter' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'leave' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'motion' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'resized' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)) #@UndefinedVariable
        }

    def __init__(self,theme,width,height):
        Widget.GroupWidget.__init__(self)
        self._width = width
        self._height = height
        self.pressed = False
        clutter.Group.__init__(self)
        self._realx = self._oldgetx()
        self._realy = self._oldgety()
        self.theme = theme
        self.themepath=(self.appdatadir+"/Themes/" + theme)
        guixmlfile = open(self.themepath + "/GUI.xml")
        guixml = ET.XML(guixmlfile.read())
        self.buttonxml = guixml.find("button")
        self.outxml = self.buttonxml.find("out")
        self.inxml = self.buttonxml.find("in")
        self.hoverxml = self.buttonxml.find("hover")
        self._textures = []
        self.makestates()
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
            event.y = event.y/(float(pycluttertk._stage.get_height())/pycluttertk._resolution[1])
            event.x = event.x/(float(pycluttertk._stage.get_width())/pycluttertk._resolution[0])
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
                event.y = event.y/(float(pycluttertk._stage.get_height())/pycluttertk._resolution[1])
                event.x = event.x/(float(pycluttertk._stage.get_width())/pycluttertk._resolution[0])
                
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
    def makestates(self):
        for i in self._textures:
            self.remove(i)
        children = self.get_children()
        self.remove_all()
        self._in = self.makestate("in")
        self._out = self.makestate("out")
        self._hover = self.makestate("hover")
        self.add(self._in)
        self.add(self._out)
        self.add(self._hover)
        for i in children:
            self.add(i)
        self._out.show()
        self._hover.hide()
        self._in.hide()
        self._textures = (self._out,
                            self._hover,
                            self._in)
        


    def makestate(self,state):
        if state == "out":
            xml = self.outxml
        elif state == "in":
            xml = self.inxml
        elif state == "hover":
            xml = self.hoverxml
        if xml.get("type") == "gradient":
            h = max(self.get_height(),1)
            w = max(self.get_width(),1)
            button=Texture.CairoTexture(int(w), int(h))
            constraint = clutter.BindConstraint(self,clutter.BIND_SIZE,0)
            button.add_constraint(constraint)
            context = button.cairo_create()
            context.identity_matrix()
            gradient = xml.find("gradient")

            pattern = SharedFunctions.MakeGradient(gradient, h, w)
            context.set_source(pattern)
            
            rounded = xml.find("rounded")
            r = float(rounded.get("topleft"))
            context.move_to(r,0)                      # Move to A
            r = float(rounded.get("topright"))
            context.line_to(w-r,0)                    # Straight line to B
            context.curve_to(w,0,w,0,w,r)       # Curve to C, Control points are both at Q1
            r = float(rounded.get("bottomright"))
            context.line_to(w,h-r)                  # Move to D
            context.curve_to(w,h,w,h,w-r,h) # Curve to E
            r = float(rounded.get("bottomleft"))
            context.line_to(r,h)                    # Line to F
            context.curve_to(0,h,0,h,0,h-r)       # Curve to G
            r = float(rounded.get("topleft"))
            context.line_to(0,r)                      # Line to H
            context.curve_to(0,0,0,0,r,0)             # Curve to A


            #Make the outline
            path = context.copy_path()
            context.fill()
            border = xml.find("border")
            color = border.get("color")
            color = [(int(color[i]+color[i+1],16)/float(0xFF)) for i in range(0,len(color),2)]
            context.append_path(path)
            context.set_source_rgb(color[0],color[1],color[2])
            context.set_line_width(1)
            context.stroke()
            
            del(context)
        elif xml.get("type") == "image":
            image=xml.find("image")
            imagepath=image.get("file")
            button=Texture.Texture(self.themepath+"/"+imagepath)
            constraint = clutter.BindConstraint(self,clutter.BIND_SIZE,0)
            button.add_constraint(constraint)
            constraint = clutter.BindConstraint(self,clutter.BIND_POSITION,0)
            button.add_constraint(constraint)
            
        return button


class LabelButton(ImageButton):
    __gtype_name__ = 'LabelButton'

    def reallocate(self,stage,actorbox,flags):
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
        self.recenter()

    def allocationchanged(self,stage,widget):
        self.recenter()
        self.makestates()
    def allocationchanged2(self,stage,actorbox,flags):
        self.makestates()
        self.recenter()
    def recenter(self):
        #self._text.set_scale(pycluttertk._stage.get_width()/pycluttertk._resolution[0],
        #                     pycluttertk._stage.get_height()/pycluttertk._resolution[1])
        x = (self.get_width()/2)-(self._text.get_width()/2)
        y = (self.get_height()/2)-(self._text.get_height()/2)
        self._text.set_x((self.get_width()/2)-(self._text.get_width()/2))
        self._text.set_y((self.get_height()/2)-(self._text.get_height()/2))
    
    def __init__(self,theme,label=" "):
        Widget.GroupWidget.__init__(self)
        self.pressed = False
        clutter.Group.__init__(self)
        self.theme = theme
        self.themepath=(self.appdatadir+"/Themes/" + theme)
        guixmlfile = open(self.themepath + "/GUI.xml")
        guixml = ET.XML(guixmlfile.read())
        buttonxml = guixml.find("button")
        self.outxml = buttonxml.find("out")
        self.inxml = buttonxml.find("in")
        self.hoverxml = buttonxml.find("hover")

        
        self._text = Text.Label(label)
        
        self.set_width(self._text.get_width()+(self._text.get_width()/len(label)*2))
        self.set_height(self._text.get_height()*2)
        self._textures = []
        self.makestates()
        self.add(self._text)
        self._text.show()
        self.recenter()
        
        
        self.set_reactive(True)
        self.connect("button-press-event", self.clicked)
        self.connect("button-release-event", self.released)
        self.connect("enter-event", self.enter)
        self.connect("leave-event", self.leave)
        self.connect('motion-event',self.motion)
        self.connect('allocation-changed',self.allocationchanged2)
