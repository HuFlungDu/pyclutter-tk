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
            print "not connected"
            raise Errors.AddError("Can't pack more than 1 widget into a window")
        else:
            widget.set_x(0)
            widget.set_y(0)
            clutter.Group.add(self,widget)
            self.widget = widget
            self.widgetconnect = widget.connect("resized",self._widgetallocationchanged)
            print "connected"
    def _widgetallocationchanged(self,stage,widget):
        if stage.get_width() < self.get_width():
            self.set_width(max(stage.get_width(),self.get_size_request()[0]))
        else:
            self.set_width(stage.get_width())
        if stage.get_height() < self.get_height():
            self.set_height(max(stage.get_height(),self.get_size_request()[1]))
        else:
            self.set_height(stage.get_height())
        print self.get_width(),self.get_height()

        print "did get here"
    def _allocationchanged(self,stage,actorbox,flags):
        if not self.widget is None:
            self.widget.set_width(max(self.get_width(),self.widget.get_size_request()[0]))
            self.widget.set_height(max(self.get_height(),self.widget.get_size_request()[1]))
        
    def drop_widget(self):
        if not self.widget is None:
            self.remove(self.widget)
            self.widget = None
    def set_name(self,name):
        self._name=name
    def get_name(self):
        return self._name
    def __init__(self,theme,name=""):
        Widget.GroupWidget.__init__(self)
        clutter.Group.__init__(self)
        self.widget = None
        self.connect("allocation-changed",self._allocationchanged)
        self._name = name
        self._height=100
        self._width=100
        
        self.theme = theme
        self.theme = theme
        self.themepath=(self.appdatadir+"/Themes/"+theme)
        guixmlfile = open(self.themepath + "/GUI.xml")
        guixml = ET.XML(guixmlfile.read())
        windowxml = guixml.find("window")
        self.basexml = windowxml.find("base")
        self._windowtex=self.make()
        clutter.Group.add(self, self._windowtex)
        
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
            window=Texture.CairoTexture(self._height, self._width)
            constraint = clutter.BindConstraint(self,clutter.BIND_SIZE,0)
            window.add_constraint(constraint)
            constraint = clutter.BindConstraint(self,clutter.BIND_POSITION,0)
            window.add_constraint(constraint)
            context = window.cairo_create()
            context.scale(self._height, self._width)
            gradient = xml.find("gradient")
            
            pattern = SharedFunctions.MakeGradient(gradient, self._height, self._width)
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
            constraint = clutter.BindConstraint(self,clutter.BIND_SIZE,0)
            window.add_constraint(constraint)
            constraint = clutter.BindConstraint(self,clutter.BIND_POSITION,0)
            window.add_constraint(constraint)
        return window
