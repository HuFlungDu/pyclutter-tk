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
    def __init__(self):
        clutter.Stage.__init__(self)
        self.connect('button-release-event', self.releaseall)
        self.connect('allocation-changed',self.reallocate)
        self._windowmanager = None
    def set_resolution(self,width=1024,height=768):
        self._resolutionx = width
        self._resolutiony = height
    def get_resolution(self):
        return (self._resolutionx,self._resolutiony)
    def scaletores(self):
        resolution = self.get_resolution()
        for i in self.get_children():
            if hasattr(i,'scaletores'):
                i.scaletores()
            elif hasattr(i,'set_scale'):
                i.set_scale(float(stage.get_width)/resolution[0],float(stage.get_height)/resolution[1])
    def releaseall(self,stage, event):
        for i in stage.get_children():
            i.releaseall(stage,event)
    def set_window_manager(self,manager):
        self._windowmanager=manager
    def add_window(self,window):
        managedwindow = self._windowmanager.add_window(window)
        self.add(managedwindow)
