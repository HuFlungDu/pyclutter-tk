import clutter
import cairo
import gobject
import SharedFunctions
import pycluttertk
from pycluttertk import Errors

from xml.etree import ElementTree as ET
import Texture
import Widget





class Window(Widget.GroupWidget,clutter.Group):
    __gtype_name__ = 'Window'
    __gsignals__ = {
                    'clicked' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                    'released' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                    'enter' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                    'leave' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                    'motion' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ), #@UndefinedVariable
                    'kill' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_PYOBJECT,)), #@UndefinedVariable
                    'resized' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)) #@UndefinedVariable
        }
    def add(self,widget):
        if not self.widget is None:
            raise Errors.AddError("Can't pack more than 1 widget into a window")
        else:
            clutter.Group.add(self,widget)
            self.widget = widget
            self.widgetconnect = widget.connect("resized",self._widgetallocationchanged)
    def _widgetallocationchanged(self,stage,widget):
        if stage.get_width() < self.get_width():
            self.set_width(max(stage.get_width(),self.get_size_request()[0]))
        else:
            self.set_width(stage.get_width())
        if stage.get_height() < self.get_height():
            self.set_height(max(stage.get_height(),self.get_size_request()[1]))
        else:
            self.set_height(stage.get_height())
        #print self.get_height(), stage.get_height()
        #self.make()
    def _allocationchanged(self,stage,actorbox,flags):
        if not self.widget is None:
            self.widget.set_width(max(self.get_width(),self.widget.get_size_request()[0]))
            self.widget.set_height(max(self.get_height(),self.widget.get_size_request()[1])) 
        self.make()
        
    def drop_widget(self):
        if not self.widget is None:
            self.remove(self.widget)
            self.widget = None
    def set_name(self,name):
        self._name=name
    def get_name(self):
        return self._name
    def __init__(self,theme,name="",height = 100, width = 100):
        Widget.GroupWidget.__init__(self)
        clutter.Group.__init__(self)
        self.widget = None
        self.connect("allocation-changed",self._allocationchanged)
        self._name = name
        self.set_height(height)
        self.set_width(width)
        
        self.theme = theme
        self.themepath=(self.appdatadir+"/Themes/"+theme)
        guixmlfile = open(self.themepath + "/GUI.xml")
        guixml = ET.XML(guixmlfile.read())
        windowxml = guixml.find("window")
        self.basexml = windowxml.find("base")
        self._windowtex = None
        self.make()
        
        
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
        if self._windowtex != None:
            self.remove(self._windowtex)
        widget = self.widget
        self.remove_all()
        self.drop_widget()
        self._windowtex = self.makestate()
        clutter.Group.add(self, self._windowtex)
        if widget != None:
            self.add(widget)
    def makestate(self):
        
        xml = self.basexml
        if xml.get("type") == "gradient":
            h = max(self.get_height(),1)
            w = max(self.get_width(),1)
            window=Texture.CairoTexture(int(w), int(h))
            constraint = clutter.BindConstraint(self,clutter.BIND_SIZE,0)
            window.add_constraint(constraint)
            constraint = clutter.BindConstraint(self,clutter.BIND_POSITION,0)
            window.add_constraint(constraint)
            context = window.cairo_create()
            gradient = xml.find("gradient")
            
            pattern = SharedFunctions.MakeGradient(gradient, h, w)
            context.set_source(pattern)
            
            context.move_to(0,0)                    
            context.line_to(w,0)
            context.line_to(w,h)
            context.line_to(0,h)
            context.line_to(0,0)
            context.fill()
            del(context)
        elif xml.get("type") == "image":
            image=xml.find("image")
            imagepath=image.get("file")
            window=Texture.Texture(self.themepath+"/"+imagepath)
            constraint = clutter.BindConstraint(self,clutter.BIND_SIZE,0)
            window.add_constraint(constraint)
            constraint = clutter.BindConstraint(self,clutter.BIND_POSITION,0)
            window.add_constraint(constraint)
        return window
