###### Gui Setup ######
from player import *
import card
import setup
import random
import Tkinter
import string
import time

p = ""
p1 = ""
p2 = ""
p3 = ""
p4 = ""
w1 = ""
w2 = ""
w3 = ""
w4 = ""

app = ""
card_chosen = card.make_card("2","Clubs")
back = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/back.gif"
single_player = False

class Gui(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize_points()
        self.initialize_cards()
        self.initialize_menu()

    def initialize_points(self):
        global p
        global p1
        global p2
        global p3
        global p4

        self.grid()

        button = Tkinter.Button(self,text="Next Play!", command=setup.NextPlay)
        button.grid(column=0,row=0)

        p = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=p)
        label.grid(column=1,row=0)
        p.set("Player Leading: " + str(setup.turn_order[0].name));

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

    def initialize_cards(self):
        global w1
        global w2
        global w3
        global w4
        global back

        """Initialize card display"""
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

    def initialize_menu(self):
        """Initialize menu bar """
        menu = Tkinter.Menu(self)
        self.config(menu=menu)

        filemenu = Tkinter.Menu(menu)
        statsmenu = Tkinter.Menu(menu)

        filemenu.add_command(label="Exit", command=self.onExit)
        filemenu.add_command(label="New Single Player Game", command=single_player_game)
        filemenu.add_command(label="New Simulation Game", command=simulation)
        menu.add_cascade(label="File", menu=filemenu)

        statsmenu.add_command(label="Stats", command=self.stats_window)
        menu.add_cascade(label="Stats", menu=statsmenu)

    def onExit(self):
        self.quit()

    def stats_window(self):
        t = Tkinter.Toplevel(self)
        t.wm_title("Game Stats")
        t.geometry("450x325")
        t.configure(bg="light slate gray")

        for i in range(4):
            x = Tkinter.StringVar()
            label = Tkinter.Label(t, textvariable=x,font=("helvetica",12,"bold"), bg="light slate gray")
            label.grid(column=i,row=1)
            x.set("Player " + str(i+1) + ": " + str(which_player(i).Points));
        for i in range(4):
            j = 2
            player = which_player(i)
            for x in player.Hand:
                y = Tkinter.StringVar()
                label = Tkinter.Label(t, textvariable=y,bg = "light slate gray")
                label.grid(column=i,row=j)
                sort = sorted(player.Hand,key=lambda x: (x.suit,x.value))
                y.set(x.name + " of " + x.suit)
                j += 1

    def update_image(self,card,player):
        global w1
        global w2
        global w3
        global w4

        file_name = get_file_path(card)
        if player.name == 1:
            img1 = Tkinter.PhotoImage(file=file_name)
            w1.configure(image = img1)
            w1.image = img1
        elif player.name == 2:
            img2 = Tkinter.PhotoImage(file=file_name)
            w2.configure(image = img2)
            w2.image = img2
        elif player.name == 3:
            img3 = Tkinter.PhotoImage(file=file_name)
            w3.configure(image = img3)
            w3.image = img3
        else:
            img4 = Tkinter.PhotoImage(file=file_name)
            w4.configure(image = img4)
            w4.image = img4

    def reset_cards(self):
        global back
        file_name = back

        img1 = Tkinter.PhotoImage(file=file_name)
        w1.configure(image = img1)
        w1.image = img1

        img2 = Tkinter.PhotoImage(file=file_name)
        w2.configure(image = img2)
        w2.image = img2

        img3 = Tkinter.PhotoImage(file=file_name)
        w3.configure(image = img3)
        w3.image = img3

        img4 = Tkinter.PhotoImage(file=file_name)
        w4.configure(image = img4)
        w4.image = img4

    def update_points(self):
        for x in setup.cards_on_table:
            if x[0].name == 1:
                p1.set("Player1: " + str(setup.player1.Points))
            elif x[0].name == 2:
                p2.set("Player2: " + str(setup.player2.Points))
            elif x[0].name == 3:
                p3.set("Player3: " + str(setup.player3.Points))
            else:
                p4.set("Player4: " + str(setup.player4.Points))

def get_file_path(card):
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

def single_player_game():
    global app
    global single_player

    app.destroy()

    single_player = True
    setup.setup()

    app = Gui(None)
    app.geometry("300x300")
    app.title("Hearts")
    app.mainloop()

def simulation():
    global app
    global single_player

    app.destroy()

    single_player = False
    setup.setup()

    app = Gui(None)
    app.geometry("300x300")
    app.title("Hearts")
    app.mainloop()
