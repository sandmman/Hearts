import gui
import configure
import Tkinter

if __name__ == "__main__":
    configure.setup()
    #configure.user_player = True

    gui.app = gui.gui(None)
    gui.app.geometry("300x300")
    gui.app.title("Hearts")
    gui.app.mainloop()
