import clutter
import Button
import Window
import GUI
global pressedposx
global pressedposy
pressedposx = 0
pressedposy = 0

def clicknewbutton(stage, event):
    global pressedposx
    global pressedposy
    pressedposx = event.x
    pressedposy = event.y
def newbuttonmotion(stage,event):
    global pressedposx
    global pressedposy
    if stage.pressed:
        stage.set_x(stage.get_x()+event.x-pressedposx)
        stage.set_y(stage.get_y()+event.y-pressedposy)
        pressedposx = event.x
        pressedposy = event.y
def clickwindow(stage, event):
    print stage.get_width()

        
def main():
    clutter.set_motion_events_enabled(True)
    newbutton = Button.LabelButton("snesOS","This is a big button")
    newwindow = Window.Window("snesOS","First window test")
    newwindow.set_width(200)
    newwindow.set_height(200)
    #newwindow.add(newbutton)
    
    stage = GUI.GUI()
    stage.set_color(clutter.Color(red=0xff, green=0xcc, blue=0xcc, alpha=0xff))
    #stage.set_size(width=1024, height=768)
    stage.set_resolution(width=1024,height=768)
    stage.add_window(newwindow)
    newwindow.connect("clicked",clickwindow)
    #stage.add(newbutton)

    newbutton.show()
    newbutton.connect("clicked",clicknewbutton)
    newbutton.connect("motion",newbuttonmotion)
    stage.set_user_resizable(True)
    stage.show()
    stage.connect('destroy', clutter.main_quit)

    clutter.main()
main()
