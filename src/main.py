import gui
import setup
import Tkinter

if __name__ == "__main__":
    setup.setup()
    #setup.user_player = True

    gui.app = gui.Gui(None)
    gui.app.geometry("300x300")
    gui.app.title("Hearts")
    gui.app.mainloop()
