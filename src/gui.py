###### gui configure ######
import card
import random
import Tkinter as tk
import string
import time
import configure

p = ""
p1 = ""
p2 = ""
p3 = ""
p4 = ""
w1 = ""
w2 = ""
w3 = ""
w4 = ""
var = ""
button = ""
z = ""

app = ""
card_chosen = card.make_card("2","Clubs")
back = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/back.gif"

class Gui(tk.Tk):

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize_points()
        self.initialize_cards()
        self.initialize_menu()
        self.p = ""
        self.p1 = ""
        self.p2 = ""
        self.p3 = ""
        self.p4 = ""
        self.w1 = ""
        self.w2 = ""
        self.w3 = ""
        self.w4 = ""
        self.button = ""

    def initialize_points(self):
        global p
        global p1
        global p2
        global p3
        global p4
        global app
        global var
        global z
        global button

        self.grid()
        # Simulation
        if configure.game.user_player == False:
            button = tk.Button(self,text="Next Play!", command=configure.game.NextPlay)
            button.grid(column=0,row=0)
        # Single Player
        else:
            button = tk.Button(self,text="Next Play!", command= lambda: self.user_play(configure.game.turn_order))
            button.grid(column=0,row=0)

            var = tk.StringVar()
            ls = [y.name + " of " + y.suit for y in configure.game.player1.Hand]
            var.set("Choose Card")
            z = tk.OptionMenu(self, var, *ls).grid(column=0,row=5)

            ready = tk.Button(self,text="Selected!", command=self.set_normal)
            ready.grid(column=1,row=5)

            if configure.game.turn_order[0].name == 1:
                button.config(state="disabled")

        p = tk.StringVar()
        label = tk.Label(self, textvariable=p)
        label.grid(column=1,row=0)
        p.set("Player Leading: " + str(configure.game.turn_order[0].name));

        """Initialize Player/Point Labels"""

        p1 = tk.StringVar()
        label = tk.Label(self, textvariable=p1, fg="Purple")
        label.grid(column=0,row=1)
        p1.set("player1: 0");

        p2 = tk.StringVar()
        label2 = tk.Label(self, textvariable=p2,fg="Green")
        label2.grid(column=1,row=1)
        p2.set("player2 : 0");

        p3 = tk.StringVar()
        label3 = tk.Label(self, textvariable=p3, fg="Red")
        label3.grid(column=1,row=3)
        p3.set("player3: 0");

        p4 = tk.StringVar()
        label4 = tk.Label(self, textvariable=p4, fg="Blue")
        label4.grid(column=0,row=3)
        p4.set("player4: 0");

    def initialize_cards(self):
        global w1
        global w2
        global w3
        global w4

        back = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/back.gif"

        """Initialize card display"""
        card = tk.PhotoImage(file=back)
        w1 = tk.Label(self, image=card)
        w1.image = card
        w1.grid(column=0,row=2)

        card2 = tk.PhotoImage(file=back)
        w2 = tk.Label(self, image=card2)
        w2.image = card2
        w2.grid(column=1,row=2)

        card3 = tk.PhotoImage(file=back)
        w3 = tk.Label(self, image=card3)
        w3.image = card3
        w3.grid(column=1,row=4)

        card4 = tk.PhotoImage(file=back)
        w4 = tk.Label(self, image=card4)
        w4.image = card4
        w4.grid(column=0,row=4)

    def initialize_menu(self):
        """Initialize menu bar """
        menu = tk.Menu(self)
        self.config(menu=menu)

        filemenu = tk.Menu(menu)
        statsmenu = tk.Menu(menu)

        filemenu.add_command(label="Exit", command=self.onExit)
        filemenu.add_command(label="New Single Player Game", command=single_player_game)
        filemenu.add_command(label="New Simulation Game", command=simulation)
        menu.add_cascade(label="File", menu=filemenu)

        statsmenu.add_command(label="Stats", command=self.stats_window)
        menu.add_cascade(label="Stats", menu=statsmenu)

    def onExit(self):
        self.quit()

    def stats_window(self):
        t = tk.Toplevel(self)
        t.wm_title("Game Stats")
        t.geometry("450x325")
        t.configure(bg="light slate gray")

        for i in range(4):
            x = tk.StringVar()
            label = tk.Label(t, textvariable=x,font=("helvetica",12,"bold"), bg="light slate gray")
            label.grid(column=i,row=1)
            x.set("Player " + str(i+1) + ": " + str(which_player(i).Points));
        for i in range(4):
            j = 2
            player = which_player(i)
            for x in player.Hand:
                y = tk.StringVar()
                label = tk.Label(t, textvariable=y,bg = "light slate gray")
                label.grid(column=i,row=j)
                sort = sorted(player.Hand,key=lambda x: (x.suit,x.value))
                y.set(x.name + " of " + x.suit)
                j += 1

    def update_options(self):
        global z
        z.grid_forget()

        var = tk.StringVar()
        ls = [y.name + " of " + y.suit for y in configure.game.player1.Hand]
        var.set("Choose Card")
        z = tk.OptionMenu(self, var, *ls).grid(column=0,row=5)

    def update_image(self,card,player):
        global w1
        global w2
        global w3
        global w4

        file_name = get_file_path(card)
        if player.name == 1:
            img1 = tk.PhotoImage(file=file_name)
            w1.configure(image = img1)
            w1.image = img1
        elif player.name == 2:
            img2 = tk.PhotoImage(file=file_name)
            w2.configure(image = img2)
            w2.image = img2
        elif player.name == 3:
            img3 = tk.PhotoImage(file=file_name)
            w3.configure(image = img3)
            w3.image = img3
        else:
            img4 = tk.PhotoImage(file=file_name)
            w4.configure(image = img4)
            w4.image = img4

    def reset_cards(self):
        back = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/back.gif"

        img1 = tk.PhotoImage(file=back)
        w1.configure(image = img1)
        w1.image = img1

        img2 = tk.PhotoImage(file=back)
        w2.configure(image = img2)
        w2.image = img2

        img3 = tk.PhotoImage(file=back)
        w3.configure(image = img3)
        w3.image = img3

        img4 = tk.PhotoImage(file=back)
        w4.configure(image = img4)
        w4.image = img4

    def update_points(self):
        """
            Updates Gui Score Output
        """
        for x in configure.game.cards_on_table:
            if x[0].name == 1:
                p1.set("player1: " + str(configure.game.player1.Points))
            elif x[0].name == 2:
                p2.set("player2: " + str(configure.game.player2.Points))
            elif x[0].name == 3:
                p3.set("player3: " + str(configure.game.player3.Points))
            else:
                p4.set("player4: " + str(configure.game.player4.Points))

    def set_normal(self):
        """
            Allows the user to play once his card is chosen and is valid
        """
        global card_chosen
        global button

        if self.fair_play(card_chosen):
            button.config(state="normal")

    def set_disabled(self):
        global button
        """
            Used in conjustion with tk - sets ready status
        """
        button.config(state="disable")

    def fair_play(self,card_played):
            """
                Ensures valid play
            """
            if card_played.suit == configure.game.suit_led or len(self.suits_in_hand(card_played)):
                return True
            else:
                return False

    def suits_in_hand(self,card):
        """
            returns user cards of same suit
        """
        if card.suit == "Clubs":
            return configure.game.player1.Clubs
        elif card.suit == "Spades":
            return configure.game.player1.Spades
        elif card.suit == "Hearts":
            return configure.game.player1.Hearts
        else:
            return configure.game.player1.Diamonds

    def user_play(self,order):
        global p
        global var
        global card_chosen

        # If the next player to go is the user player -> lock the NextPlay button
        if configure.game.turn < 3 and order[configure.game.turn+1].name == 1:
            self.set_disabled()
        else:
            self.set_normal()

        if len(configure.game.deck) == 0:
            self.stats_window()
        # Check if hand is over
        if len(configure.game.cards_on_table) == 4:
            configure.game.cards_on_table = []
            configure.game.turn = 0
            self.reset_cards()

        p.set("Player Leading: " + str(configure.game.turn_order[0].name));

        if order[configure.game.turn].name == 1:
            temp = var.get().split(" ")
            card_chosen = card.make_card(temp[0],temp[2])

        configure.game.play(order[configure.game.turn],card_chosen)
        self.update_image(configure.game.cards_on_table[-1][1],configure.game.cards_on_table[-1][0])

        if len(configure.game.cards_on_table) == 4:
            self.update_points()

        configure.game.turn += 1
        self.update_options()

def get_file_path(card):
    """
        Gets the path for a given card.
    """
    card_file = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/"
    f = card.name + "OF" + card.suit + ".gif"
    card_file = card_file + f
    return card_file

def which_player(i):
    """Returns the given player"""
    if i == 0:
        return configure.game.player1
    elif i == 1:
        return configure.game.player2
    elif i == 2:
        return configure.game.player3
    else:
        return configure.game.player4

def single_player_game():
    """Creates a new single player game"""
    global app

    app.destroy()

    configure.setup(True)

    app = Gui(None)
    app.geometry("300x300")
    app.title("Hearts")
    app.mainloop()

def simulation():
    """Creates a new simulation"""
    global app

    app.destroy()

    configure.setup(False)

    app = Gui(None)
    app.geometry("300x300")
    app.title("Hearts")
    app.mainloop()
