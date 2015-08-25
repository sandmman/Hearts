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

        """Initialize Player/Point Labels"""

        p1 = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=p1, fg="Purple")
        label.grid(column=0,row=1)
        p1.set("Player1: " + str(setup.player1.Points));

        p2 = Tkinter.StringVar()
        label2 = Tkinter.Label(self, textvariable=p2,fg="Green")
        label2.grid(column=1,row=1)
        p2.set("Player2 : " + str(setup.player2.Points));

        p3 = Tkinter.StringVar()
        label3 = Tkinter.Label(self, textvariable=p3, fg="Red")
        label3.grid(column=1,row=3)
        p3.set("Player3: " + str(setup.player3.Points));

        p4 = Tkinter.StringVar()
        label4 = Tkinter.Label(self, textvariable=p4, fg="Blue")
        label4.grid(column=0,row=3)
        p4.set("Player4: " + str(setup.player4.Points));

        """Initialize card display"""
        back = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/back.gif"
        card = Tkinter.PhotoImage(file=back)
        w1 = Tkinter.Label(self, image=card)
        w1.image = card
        w1.grid(column=0,row=2)

        card2 = Tkinter.PhotoImage(file=back)
        w2 = Tkinter.Label(self, image=card2)
        w2.image = card2
        w2.grid(column=1,row=2)

        card3 = Tkinter.PhotoImage(file=back)
        w3 = Tkinter.Label(self, image=card3)
        w3.image = card3
        w3.grid(column=1,row=4)

        card4 = Tkinter.PhotoImage(file=back)
        w4 = Tkinter.Label(self, image=card4)
        w4.image = card4
        w4.grid(column=0,row=4)


        """Initialize menu bar """
        menu = Tkinter.Menu(self)
        self.config(menu=menu)

        filemenu = Tkinter.Menu(menu)
        statsmenu = Tkinter.Menu(menu)

        filemenu.add_command(label="Exit", command=self.onExit)
        menu.add_cascade(label="File", menu=filemenu)

        statsmenu.add_command(label="Stats", command=self.stats_window)
        menu.add_cascade(label="Stats", menu=statsmenu)



    def onExit(self):
        self.quit()
    def stats_window(self):
        t = Tkinter.Toplevel(self)
        t.wm_title("Game Stats")
        t.geometry("450x325")
        l = Tkinter.Label(t,text="Current Game",font=("helvetica",16))
        l.grid(column=0,row=0)
        for i in range(4):
            x = Tkinter.StringVar()
            label = Tkinter.Label(t, textvariable=x, bg="light grey")
            label.grid(column=i,row=1)
            x.set("Player " + str(i) + ": " + str(which_player(i).Points));
        for i in range(4):
            for j in range(3,len(setup.player1.Hand)+3):
                y = Tkinter.StringVar()
                label = Tkinter.Label(t, textvariable=y,)
                label.grid(column=i,row=j)
                sort = sorted(which_player(i).Hand,key=lambda x: (x.suit,x.value))
                y.set(sort[j-3].name + " of " + sort[j-3].suit);

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

def which_player(i):
    if i == 0:
        return setup.player1
    elif i == 1:
        return setup.player2
    elif i == 2:
        return setup.player3
    else:
        return setup.player4


if __name__ == "__main__":
    app = Gui(None)
    app.geometry("300x300")
    app.title("Hearts")

    setup.setup()
    app.mainloop()
