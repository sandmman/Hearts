import gui
import configure
import Tkinter

if __name__ == "__main__":
    configure.setup(False)

    gui.app = gui.Gui(None)
    gui.app.geometry("275x300")
    gui.app.title("Hearts")
    gui.app.mainloop()
