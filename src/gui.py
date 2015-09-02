###### gui configure ######
import card
import random
import Tkinter as tk
import string
import time
import configure

app = ""


class Gui(tk.Tk):

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize_points()
        self.initialize_cards()
        self.initialize_menu()
        self.card_chosen = card.make_card("2","Clubs")

    def initialize_points(self):
        global app

        self.grid()
        # Simulation
        if configure.game.user_player == False:
            self.button = tk.Button(self,text="Next Play!", command=configure.game.NextPlay)
            self.button.grid(column=0,row=0)
        # Single Player
        else:
            self.button = tk.Button(self,text="Next Play!", command= lambda: self.user_play(configure.game.turn_order))
            self.button.grid(column=0,row=0)

            self.var = tk.StringVar()
            ls = [self.shape(y) + " " + y.name + " of " + y.suit for y in sorted(configure.game.player1.Hand,key=lambda x : (x.suit,x.value))]
            self.var.set("Choose Card")
            self.optmenu = tk.OptionMenu(self, self.var, *ls)
            self.optmenu.grid(column=0,row=5)

            ready = tk.Button(self,text="Selected!", command=self.set_normal)
            ready.grid(column=1,row=5)

            if configure.game.turn_order[0].name == 1:
                self.button.config(state="disabled")

        self.p = tk.StringVar()
        label = tk.Label(self, textvariable=self.p)
        label.grid(column=1,row=0)
        self.p.set("Player " + str(configure.game.turn_order[0].name) + " has 2 of clubs ");

        """Initialize Player/Point Labels"""

        self.p1 = tk.StringVar()
        label = tk.Label(self, textvariable=self.p1, fg="Purple")
        label.grid(column=0,row=1)
        self.p1.set("player1: 0");

        self.p2 = tk.StringVar()
        label2 = tk.Label(self, textvariable=self.p2,fg="Green")
        label2.grid(column=1,row=1)
        self.p2.set("player2 : 0");

        self.p3 = tk.StringVar()
        label3 = tk.Label(self, textvariable=self.p3, fg="Red")
        label3.grid(column=1,row=3)
        self.p3.set("player3: 0");

        self.p4 = tk.StringVar()
        label4 = tk.Label(self, textvariable=self.p4, fg="Blue")
        label4.grid(column=0,row=3)
        self.p4.set("player4: 0");

    def initialize_cards(self):
        """Initialize card display"""
        back = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/back.gif"

        card = tk.PhotoImage(file=back)
        self.w1 = tk.Label(self, image=card)
        self.w1.image = card
        self.w1.grid(column=0,row=2)

        card2 = tk.PhotoImage(file=back)
        self.w2 = tk.Label(self, image=card2)
        self.w2.image = card2
        self.w2.grid(column=1,row=2)

        card3 = tk.PhotoImage(file=back)
        self.w3 = tk.Label(self, image=card3)
        self.w3.image = card3
        self.w3.grid(column=1,row=4)

        card4 = tk.PhotoImage(file=back)
        self.w4 = tk.Label(self, image=card4)
        self.w4.image = card4
        self.w4.grid(column=0,row=4)

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
        t.geometry("500x325")
        t.configure(bg="light slate gray")

        for i in range(4):
            x = tk.StringVar()
            label = tk.Label(t, textvariable=x,font=("helvetica",12,"bold","underline"), bg="light slate gray")
            label.grid(column=i,row=1)
            x.set("Player " + str(i+1) + ": " + str(which_player(i).Points));
        for i in range(4):
            j = 2
            player = which_player(i)
            for x in sorted(player.Hand,key=lambda x: (x.suit,x.value)):
                y = tk.StringVar()
                label = tk.Label(t, textvariable=y,bg = "light slate gray",fg = self.color(x))
                label.grid(column=i,row=j)
                y.set(self.shape(x) + " " + x.name + " of " + x.suit)
                j += 1

    def color(self,card):
        if card.suit == "Clubs":
            return "black"
        elif card.suit == "Spades":
            return "purple"
        elif card.suit == "Diamonds":
            return "red"
        else:
            return "pink"

    def shape(self,card):
        if card.suit == "Clubs":
            return u"\u2663"
        elif card.suit == "Spades":
            return u"\u2660"
        elif card.suit == "Diamonds":
            return u"\u25C6"
        else:
            return u"\u2661"

    def update_optionmenu(self):
        self.optmenu["menu"].delete(0,"end")
        self.var.set("Choose Card")

        for card in sorted(configure.game.player1.Hand, key=lambda x: (x.suit,x.name)):
            c = self.shape(card) + " " + card.name + " of " + card.suit
            self.optmenu["menu"].add_command(label=c, command=lambda temp = c: self.optmenu.setvar(self.optmenu.cget("textvariable"), value = temp))

    def update_image(self,card,player):
        file_name = get_file_path(card)
        if player.name == 1:
            img1 = tk.PhotoImage(file=file_name)
            self.w1.configure(image = img1)
            self.w1.image = img1
        elif player.name == 2:
            img2 = tk.PhotoImage(file=file_name)
            self.w2.configure(image = img2)
            self.w2.image = img2
        elif player.name == 3:
            img3 = tk.PhotoImage(file=file_name)
            self.w3.configure(image = img3)
            self.w3.image = img3
        else:
            img4 = tk.PhotoImage(file=file_name)
            self.w4.configure(image = img4)
            self.w4.image = img4

    def reset_cards(self):
        back = "/Users/aaronliberatore/Documents/cardCounting/classic-cards/back.gif"

        img1 = tk.PhotoImage(file=back)
        self.w1.configure(image = img1)
        self.w1.image = img1

        img2 = tk.PhotoImage(file=back)
        self.w2.configure(image = img2)
        self.w2.image = img2

        img3 = tk.PhotoImage(file=back)
        self.w3.configure(image = img3)
        self.w3.image = img3

        img4 = tk.PhotoImage(file=back)
        self.w4.configure(image = img4)
        self.w4.image = img4

    def update_points(self):
        """
            Updates Gui Score Output
        """
        for x in configure.game.cards_on_table:
            if x[0].name == 1:
                self.p1.set("player1: " + str(configure.game.player1.Points))
            elif x[0].name == 2:
                self.p2.set("player2: " + str(configure.game.player2.Points))
            elif x[0].name == 3:
                self.p3.set("player3: " + str(configure.game.player3.Points))
            else:
                self.p4.set("player4: " + str(configure.game.player4.Points))

    def set_normal(self):
        """
            Allows the user to play once his card is chosen and is valid
        """
        # Always set to normal in a simulation game
        # See if its the users turn
        if  configure.game.turn_order[configure.game.turn].name == 1:
            temp = self.var.get().split(" ")
            self.card_chosen = card.make_card(temp[1],temp[3])
        # Single Player: Check to see if card picked is legal
        if self.fair_play(self.card_chosen):
            self.button.config(state="normal")

    def set_enabled(self):
        self.button.config(state="normal")

    def set_disabled(self):
        """
            Used in conjustion with tk - sets ready status
        """
        self.button.config(state="disable")

    def fair_play(self,card_played):
        """
            Ensures valid play
        """
        if card_played.suit == configure.game.suit_led or len(self.suits_in_hand(configure.game.suit_led)) == 0 or configure.game.turn_order[configure.game.turn].name == 1:
            return True
        else:
            return False

    def suits_in_hand(self,suit):
        """
            returns user cards of same suit
        """
        if suit == "Clubs":
            return configure.game.player1.Clubs
        elif suit == "Spades":
            return configure.game.player1.Spades
        elif suit == "Hearts":
            return configure.game.player1.Hearts
        else:
            return configure.game.player1.Diamonds
    def lock_status(self,order):
        """Enables or Disables lock based on next turn"""
        # User players turn is comming up
        temp = configure.game.turn + 1
        if configure.game.turn < 3 and order[temp].name == 1 and configure.game.user_player:
            self.set_disabled()
        elif len(configure.game.cards_on_table) == 4 and order[0].name == 1 and configure.game.user_player:
            self.set_disabled()
        else:
            self.set_enabled()

    def user_play(self,order):

        self.p.set("Player " + str(configure.game.turn_order[0].name) + " Led " + configure.game.suit_led );

        # Check if Game Over
        if len(configure.game.deck) == 0:
            self.stats_window()
        # Check if hand is over
        if len(configure.game.cards_on_table) == 4:
            configure.game.cards_on_table = []
            #configure.game.turn = 0
            self.reset_cards()

        configure.game.play(order[configure.game.turn],self.card_chosen)
        self.update_image(configure.game.cards_on_table[-1][1],configure.game.cards_on_table[-1][0])


        # Set gui NextPLay lock status for next turn
        self.lock_status(configure.game.turn_order)
        configure.game.turn += 1
        self.update_optionmenu()

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
