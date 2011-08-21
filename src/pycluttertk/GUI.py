import clutter
import gobject


class GUI(clutter.Stage):
    _resolutionx = 1024
    _resolutiony = 768
    def reallocate(self,stage,actorbox,flags):
        self.height = actorbox.y2 - actorbox.y1
        self.width = actorbox.x2 - actorbox.x1
        for i in self.get_children():
            i.reallocate(self,actorbox,flags)
    def __init__(self, windowmanager = None):
        clutter.Stage.__init__(self)
        self.connect('button-release-event', self.releaseall)
        self.connect('allocation-changed',self.reallocate)
        if windowmanager != None:
            self._windowmanager = windowmanager
        else:
            import StandardWindowManager
            self._windowmanager = StandardWindowManager.WindowManager()
                    
        
        
    def set_resolution(self,width=1024,height=768):
        self._resolutionx = width
        self._resolutiony = height
        self.reallocate(self,clutter.ActorBox(0,0,self.get_width(),self.get_height())
                        ,clutter.AllocationFlags(0))
    def get_resolution(self):
        return (self._resolutionx,self._resolutiony)
    def releaseall(self,stage, event):
        for i in stage.get_children():
            i.releaseall(stage,event)
    def set_window_manager(self,manager):
        self._windowmanager=manager
    def add_window(self,window):
        managedwindow = self._windowmanager.add_window(window)
        self.add(managedwindow)
