import clutter
import pycluttertk
global guistage

def clicknewbutton(stage, event):
    print event
    pass
    #newbutton2 = pycluttertk.LabelButton("snesOS","I test packing")
    #vbox.pack(newbutton2,True,True,True,
    #                 clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    

        
def main():
    global guistage
    global vbox
    pycluttertk.reload_settings()
    guistage = pycluttertk.GUI()
    #clutter.set_motion_events_enabled(True)
    newbutton = pycluttertk.LabelButton("snesOS","This is a big button")
    newbutton2 = pycluttertk.LabelButton("snesOS","This is also a big button")
    newwindow = pycluttertk.Window("snesOS","First window test",)
    #newwindow.set_width(300)
    #newwindow.set_height(200)
    newwindow.request_size(300,200)
    mainmenu = pycluttertk.Menu("snesOS")
    mainmenu.set_height(20)
    mainmenu.connect("clicked",clicknewbutton)
    vbox = pycluttertk.VBox()
    hbox = pycluttertk.HBox()
    newwindow.add(vbox)
    vbox.pack(mainmenu,False,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    vbox.pack(hbox,False,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    hbox.pack(newbutton,False,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    hbox.pack(newbutton2,False,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    newbutton3 = pycluttertk.LabelButton("snesOS","I test packing")
    vbox.pack(newbutton3,False,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    newbutton4 = pycluttertk.LabelButton("snesOS","I test packing")
    vbox.pack(newbutton4,False,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    newbutton5 = pycluttertk.LabelButton("snesOS","I test packing")
    vbox.pack(newbutton5,False,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)
    newbutton6 = pycluttertk.LabelButton("snesOS","I test packing")
    vbox.pack(newbutton6,False,True,True,
                     clutter.BOX_ALIGNMENT_CENTER,clutter.BOX_ALIGNMENT_CENTER)

    
    guistage.set_color(clutter.Color(red=0xff, green=0xcc, blue=0xcc, alpha=0xff))
    #stage.set_size(width=1024, height=768)
    guistage.set_resolution(width=1024,height=768)
    guistage.add_window(newwindow)
    #newwindow.connect("clicked",clickwindow)
    #stage.add(newbutton)

    #newbutton.show()=
    newbutton.connect("clicked",clicknewbutton)
    #newbutton.connect("motion",newbuttonmotion)
    guistage.set_user_resizable(True)
    #guistage.show()
    guistage.connect('destroy', clutter.main_quit)
    clutter.main()
if __name__ == "__main__":
    main()
