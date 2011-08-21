import clutter
import pycluttertk
global guistage

def clicknewbutton(stage, event):
    global guistage
    newbutton2 = pycluttertk.LabelButton("snesOS","I test packing")
    vbox.pack(newbutton2,True,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    

        
def main():
    global guistage
    global vbox
    #clutter.set_motion_events_enabled(True)
    newbutton = pycluttertk.LabelButton("snesOS","This is a big button")
    newbutton2 = pycluttertk.LabelButton("snesOS","This is also a big button")
    newwindow = pycluttertk.Window("snesOS","First window test")
    #newwindow.set_width(300)
    #newwindow.set_height(200)
    newwindow.request_size(300,200)
    vbox = pycluttertk.VBox()
    newwindow.add(vbox)
    vbox.pack(newbutton,True,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    vbox.pack(newbutton2,True,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    newbutton3 = pycluttertk.LabelButton("snesOS","I test packing")
    vbox.pack(newbutton3,True,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)

    guistage = pycluttertk.GUI()
    guistage.set_color(clutter.Color(red=0xff, green=0xcc, blue=0xcc, alpha=0xff))
    #stage.set_size(width=1024, height=768)
    guistage.set_resolution(width=1024,height=768)
    guistage.add_window(newwindow)
    #newwindow.connect("clicked",clickwindow)
    #stage.add(newbutton)

    newbutton.show()
    newbutton.connect("clicked",clicknewbutton)
    #newbutton.connect("motion",newbuttonmotion)
    guistage.set_user_resizable(True)
    guistage.show()
    guistage.connect('destroy', clutter.main_quit)

    clutter.main()
main()
