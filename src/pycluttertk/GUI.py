import clutter
import gobject
import pycluttertk


class GUI(clutter.Stage):
    _resolutionx = 1024
    _resolutiony = 768
    _oldadd = clutter.Stage.add
    _use_resolution = True
    def add(self,widget):
        self.mainbox.add(widget)
    def reallocate(self,stage,actorbox,flags):
        self._height = actorbox.y2 - actorbox.y1
        self._width = actorbox.x2 - actorbox.x1
        self.mainbox.set_scale(self._width/pycluttertk._resolution[0],
                                self._height/pycluttertk._resolution[1])
        
        
        #for i in self.get_children():
        #    i.reallocate(self,actorbox,flags)
    def set_use_resolution(self,useres):
        self._use_resolution = useres
    def __init__(self, windowmanager = None, width = 1024, height = 768):
        self.mainbox = clutter.Group()
        self.set_resolution(width, height)
        
        clutter.Stage.__init__(self)
        self._oldadd(self.mainbox)
        self.connect('button-release-event', self.releaseall)
        self.connect('allocation-changed',self.reallocate)
        if windowmanager != None:
            self._windowmanager = windowmanager
        else:
            import StandardWindowManager
            self._windowmanager = StandardWindowManager.WindowManager()
        
        pycluttertk._stage = self
                    
        
        
    def set_resolution(self,width=1024,height=768):
        self._resolutionx = width
        self._resolutiony = height
        pycluttertk._resolution = (self._resolutionx,self._resolutiony)
        self.reallocate(self,clutter.ActorBox(0,0,self.get_width(),self.get_height())
                        ,clutter.AllocationFlags(0))
        
    def get_resolution(self):
        return (self._resolutionx,self._resolutiony)
    def releaseall(self,stage, event):
        for i in self.mainbox.get_children():
            i.releaseall(stage,event)
    def set_window_manager(self,manager):
        self._windowmanager=manager
    def add_window(self,window):
        managedwindow = self._windowmanager.add_window(window)
        self.add(managedwindow)
