###### Gui Setup ######
from player import *
from card import *
import setup
import random
import Tkinter
import string

p = ""
p1 = ""
p2 = ""
p3 = ""
p4 = ""
w1 = ""
w2 = ""
w3 = ""
w4 = ""


class Gui(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
    def initialize(self):
        global p
        global p1
        global p2
        global p3
        global p4
        global w1
        global w2
        global w3
        global w4

        self.grid()

        button = Tkinter.Button(self,text="Next Play!", command=self.NextPlay)
        button.grid(column=0,row=0)

        p = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=p)
        label.grid(column=1,row=0)
        p.set("Player Leading: " + str(setup.leading));

        p1 = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=p1, fg="Purple")
        label.grid(column=0,row=1)
        p1.set("Player1: " + str(setup.player1.Points));

        back = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/back.gif"
        card = Tkinter.PhotoImage(file=back)
        w1 = Tkinter.Label(self, image=card)
        w1.image = card
        w1.grid(column=0,row=2)

        p2 = Tkinter.StringVar()
        label2 = Tkinter.Label(self, textvariable=p2,fg="Green")
        label2.grid(column=1,row=1)
        p2.set("Player2 : " + str(setup.player2.Points));

        card2 = Tkinter.PhotoImage(file=back)
        w2 = Tkinter.Label(self, image=card2)
        w2.image = card2
        w2.grid(column=1,row=2)

        p3 = Tkinter.StringVar()
        label3 = Tkinter.Label(self, textvariable=p3, fg="Red")
        label3.grid(column=1,row=3)
        p3.set("Player3: " + str(setup.player3.Points));

        card3 = Tkinter.PhotoImage(file=back)
        w3 = Tkinter.Label(self, image=card3)
        w3.image = card3
        w3.grid(column=1,row=4)

        p4 = Tkinter.StringVar()
        label4 = Tkinter.Label(self, textvariable=p4, fg="Blue")
        label4.grid(column=0,row=3)
        p4.set("Player4: " + str(setup.player4.Points));

        card4 = Tkinter.PhotoImage(file=back)
        w4 = Tkinter.Label(self, image=card4)
        w4.image = card4
        w4.grid(column=0,row=4)

        self.grid_columnconfigure(0,weight=1)

    def update_image(self):
        global w1
        global w2
        global w3
        global w4

        for x in setup.played:
            file_name = self.get_file_path(x[1])
            if x[0].player_num == 1:
                img1 = Tkinter.PhotoImage(file=file_name)
                w1.configure(image = img1)
                w1.image = img1
            elif x[0].player_num == 2:
                img2 = Tkinter.PhotoImage(file=file_name)
                w2.configure(image = img2)
                w2.image = img2
            elif x[0].player_num == 3:
                img3 = Tkinter.PhotoImage(file=file_name)
                w3.configure(image = img3)
                w3.image = img3
            else:
                img4 = Tkinter.PhotoImage(file=file_name)
                w4.configure(image = img4)
                w4.image = img4

    def NextPlay(self):
        global p
        global p1
        global p2
        global p3
        global p4

        if setup.run():
            p1.set("Game Over")
            p2.set("Game Over")
            p3.set("Game Over")
            p4.set("Game Over")

        p.set("Player Leading: " + str(setup.leading));

        for x in setup.played:
            self.update_image()
            if x[0].player_num == 1:
                p1.set("Player1: " + str(setup.player1.Points))
            elif x[0].player_num == 2:
                p2.set("Player2: " + str(setup.player2.Points))
            elif x[0].player_num == 3:
                p3.set("Player3: " + str(setup.player3.Points))
            else:
                p4.set("Player4: " + str(setup.player4.Points))

    def get_file_path(self,card):
        card_file = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/"
        f = card.name + "OF" + card.suit + ".gif"
        card_file = card_file + f
        return card_file

if __name__ == "__main__":
    app = Gui(None)
    app.geometry("300x300")
    app.title("Hearts")

    setup.setup()
    app.mainloop()
