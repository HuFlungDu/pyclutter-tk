import clutter
import gobject
from xml.etree import ElementTree as ET
import Texture
import Text
import Widget
import SharedFunctions
import layouters

class Menu(Widget.GroupWidget,clutter.Group):
    __gtype_name__ = 'Menu'
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
    def __init__(self,theme):
        Widget.GroupWidget.__init__(self)
        self.pressed = False
        clutter.Group.__init__(self)
        self.theme = theme
        self.themepath=(self.appdatadir+"/Themes/" + theme)
        guixmlfile = open(self.themepath + "/GUI.xml")
        guixml = ET.XML(guixmlfile.read())
        self.menuxml = guixml.find("menu")
        self.basexml = self.menuxml.find("base")
        self._texture = None
        self.makestates()
        self.set_reactive(True)
        self.connect('allocation-changed',self.allocationchanged2)
        self.connect('resized',self.allocationchanged)
        self.connect("button-press-event", self.clicked)
        self.connect("button-release-event", self.released)
        self.connect("enter-event", self.enter)
        self.connect("leave-event", self.leave)
        self.connect('motion-event',self.motion)
        
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
        
    def allocationchanged(self,stage,widget):\
        self.makestates()
    def allocationchanged2(self,stage,actorbox,flags):
        self.set_width(actorbox.x2-actorbox.x1)
        self.set_height(actorbox.y2-actorbox.y1)    
    
    def makestates(self):
        if self._texture != None:
            self.remove(self._texture)
        children = self.get_children()
        self.remove_all()
        self._texture = self.makestate()
        self.add(self._texture)
        for child in children:
            self.add(child)
        


    def makestate(self):
        
        xml = self.basexml
        if xml.get("type") == "gradient":
            h = max(self.get_height(),1)
            w = max(self.get_width(),1)
            menu=Texture.CairoTexture(int(w), int(h))
            constraint = clutter.BindConstraint(self,clutter.BIND_SIZE,0)
            menu.add_constraint(constraint)
            constraint = clutter.BindConstraint(self,clutter.BIND_POSITION,0)
            menu.add_constraint(constraint)
            context = menu.cairo_create()
            gradient = xml.find("gradient")

            pattern = SharedFunctions.MakeGradient(gradient, h, w)
            context.set_source(pattern)
            
            context.move_to(0,0)                    
            context.line_to(w,0)
            context.line_to(w,h)
            context.line_to(0,h)
            context.line_to(0,0)
            context.fill()

            #Make the outline
            path = context.copy_path()
            context.fill()
            border = xml.find("border")
            color = border.get("color")
            color = [(int(color[i]+color[i+1],16)/float(0xFF)) for i in range(0,len(color),2)]
            context.append_path(path)
            alpha = float(border.get("alpha"))
            context.set_source_rgba(color[0],color[1],color[2],alpha)
            context.set_line_width(1)
            context.stroke()
            
            del(context)
        elif xml.get("type") == "image":
            image=xml.find("image")
            imagepath=image.get("file")
            menu=Texture.Texture(self.themepath+"/"+imagepath)
            constraint = clutter.BindConstraint(self,clutter.BIND_SIZE,0)
            menu.add_constraint(constraint)
            constraint = clutter.BindConstraint(self,clutter.BIND_POSITION,0)
            menu.add_constraint(constraint)
            
        return menu
    
class MenuItem(Widget.GroupWidget,clutter.Group):
    __gtype_name__ = 'MenuItem'
    __gsignals__ = {
                'clicked' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'released' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'enter' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'leave' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'motion' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                'resized' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)) #@UndefinedVariable
        }
    def reallocate(self,stage,actorbox,flags):
        for i in self.get_children():
            i.reallocate(stage,actorbox,flags)
        self.recenter()

    def allocationchanged(self,stage,widget):
        self.recenter()
        self.makestates()
    def allocationchanged2(self,stage,actorbox,flags):
        self.set_width(actorbox.x2-actorbox.x1)
        self.set_height(actorbox.y2-actorbox.y1)
    def recenter(self):
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
        buttonxml = guixml.find("menuitem")
        self.outxml = buttonxml.find("out")
        self.inxml = buttonxml.find("in")
        self.hoverxml = buttonxml.find("hover")
        
        
        color = self.outxml.find("text").get("color")
        alpha = int(float(self.outxml.find("text").get("alpha"))*255)
        self.outtextcolor = [(int(color[i] + color[i + 1], 16)) for i in range(0, len(color), 2)]
        self.outtextcolor.append(int(alpha))
        self.outtextcolor = clutter.Color(self.outtextcolor[0],self.outtextcolor[1],self.outtextcolor[2],self.outtextcolor[3])
        
        color = self.inxml.find("text").get("color")
        alpha = int(float(self.inxml.find("text").get("alpha"))*255)
        self.intextcolor = [(int(color[i] + color[i + 1], 16)) for i in range(0, len(color), 2)]
        self.intextcolor.append(int(alpha))
        self.intextcolor = clutter.Color(self.intextcolor[0],self.intextcolor[1],self.intextcolor[2],self.intextcolor[3])
        
        color = self.hoverxml.find("text").get("color")
        alpha = int(float(self.hoverxml.find("text").get("alpha"))*255)
        self.hovertextcolor = [(int(color[i] + color[i + 1], 16)) for i in range(0, len(color), 2)]
        self.hovertextcolor.append(int(alpha))
        self.hovertextcolor = clutter.Color(self.hovertextcolor[0],self.hovertextcolor[1],self.hovertextcolor[2],self.hovertextcolor[3])
        
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
        self.connect('resized',self.allocationchanged)

        
    def releaseall(self,stage,event):
        if self.pressed:
            self._out.show()
            self._hover.hide()
            self._in.hide()
            self._text.set_color(self.outtextcolor)
            self.pressed = False
    def clicked(self,stage, event):
        if event.button==1:
            self._out.hide()
            self._hover.hide()
            self._in.show()
            self.pressed = True
            self._text.set_color(self.intextcolor)
        self.emit("clicked",event)
    def released(self,stage,event):
        if self.pressed:
            if event.button==1:
                self._out.hide()
                self._hover.show()
                self._in.hide()
                self.pressed = False
                self._text.set_color(self.outtextcolor)
                
            self.emit("released",event)
    def enter(self,stage,event):
        if self.pressed:
            self._out.hide()
            self._hover.hide()
            self._in.show()
            self._text.set_color(self.intextcolor)
        else:
            self._out.hide()
            self._hover.show()
            self._in.hide()
            self._text.set_color(self.hovertextcolor)
        self.emit("enter",event)
    def leave(self,stage,event):
        self._out.show()
        self._hover.hide()
        self._in.hide()
        self._text.set_color(self.outtextcolor)
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
            alpha = float(border.get("alpha"))
            context.set_source_rgba(color[0],color[1],color[2],alpha)
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