from player import *
from card import *
"""You have a Circular import issue with card and player"""
import random
import Tkinter
import string
import brain
import gui

#Global Variables
player1 = make_player([], 1,1)
player2 = make_player([],2,2)
player3 = make_player([],3,3)
player4 = make_player([],4,4)

already_played = []
cards_on_table = []
turn_order = []
suit_led = "Clubs"
first_hand = True
user_player = False
user_card_selected = False

"""
 Utility Functions
"""
def points_on_table():
    global cards_on_table

    points = 0
    point_cards = [x[1] for x in cards_on_table if x[1].suit == "Hearts" or (x[1].suit == "Spades" and x[1].name == "Queen")]
    for card in point_cards:
        if card.suit == "Hearts":
            points += 1
        else:
            points += 13

    return points

def get_next_turn_order():
    global turn_order
    global cards_on_table
    global first_hand
    global player1
    global player2
    global player3
    global player4

    #[(player,card_played)]
    same_suit = [x for x in cards_on_table if x[1].suit == cards_on_table[0][1].suit]
    if len(same_suit) == 1:
        turn_order = [x[0] for x in cards_on_table]
    same_suit = sorted(same_suit,key=lambda x : (x[1].value),reverse = True)
    turn_order = [same_suit[0][0]]
    if turn_order[0].name == 1:
        turn_order = [player1,player2,player3,player4]
        player1.Points = player1.Points + points_on_table()
        player1.turn_pos = 1
        player2.turn_pos = 2
        player3.turn_pos = 3
        player4.turn_pos = 4
    elif turn_order[0].name == 2:
        turn_order = [player2,player3,player4,player1]
        player2.Points = player2.Points + points_on_table()
        player1.turn_pos = 4
        player2.turn_pos = 1
        player3.turn_pos = 2
        player4.turn_pos = 3
    elif turn_order[0].name == 3:
        turn_order = [player3,player4,player1,player2]
        player3.Points = player3.Points + points_on_table()
        player1.turn_pos = 3
        player2.turn_pos = 4
        player3.turn_pos = 1
        player4.turn_pos = 2
    else:
        turn_order = [player4,player1,player2,player3]
        player4.Points = player4.Points + points_on_table()
        player1.turn_pos = 2
        player2.turn_pos = 3
        player3.turn_pos = 4
        player4.turn_pos = 1

def remove_card(player,card_played):
    new_hand = [x for x in player.Hand if not x.equals(card_played)]
    player.Hand = new_hand
    if card_played.suit == "Clubs":
        player.Clubs = [x for x in player.Clubs if not x.equals(card_played)]
        return player
    elif card_played.suit == "Spades":
        player.Spades = [x for x in player.Spades if not x.equals(card_played)]
        return player
    elif card_played.suit == "Hearts":
        player.Hearts = [x for x in player.Hearts if not x.equals(card_played)]
        return player
    else:
        player.Diamonds = [x for x in player.Diamonds if not x.equals(card_played)]
        return player

def update_player(card_played, name):
    global player1
    global player2
    global player3
    global player4

    if name == 1:
        player1 = remove_card(player1,card_played)
    if name == 2:
        player2 = remove_card(player2,card_played)
    if name == 3:
        player3 = remove_card(player3,card_played)
    if name == 4:
        player4 = remove_card(player4,card_played)

def update_deck_and_suits_arrays(card_played):
    global deck

    deck = [card for card in deck if not card.equals(card_played)]
    if card_played.suit == "Clubs":
        clubs.remove(find_in_array(card_played,clubs))
    elif card_played.suit == "Spades":
        spades.remove(find_in_array(card_played,spades))
    elif card_played.suit == "Diamonds":
        diamonds.remove(find_in_array(card_played,diamonds))
    else:
        hearts.remove(find_in_array(card_played,hearts))

def find_in_array(card_played,array):
    for card in array:
        if card.equals(card_played):
            return card

def helper(Player,card_played):
    global cards_on_table
    global suit_led

    cards_on_table.append((Player,card_played))
    if Player.turn_pos == 1:
        suit_led = card_played.suit
    update_player(card_played,Player.name)
    update_deck_and_suits_arrays(card_played)
    if len(cards_on_table) == 4:
        get_next_turn_order()
        deck_stats(deck)

def find_Card(card):
    global turn_order

    for player in turn_order:
        for c in player.Hand:
            if c.equals(card):
                return player.name
    return 0


def play(Player,card,user):
    global deck
    global first_hand
    global user_player

    user_player = user

    if len(deck) == 0:
        print "Game Over"
    if user_player and Player.name == 1:
        if Player.turn_pos == 1:
            helper(Player,card)
            first_hand = False
        else:
            helper(Player,card)
    else:
        if first_hand:
            helper(Player,make_card("2","Clubs"))
            first_hand = False
        #Player is leading
        elif Player.turn_pos == 1:
            brain.card_to_lead(Player)
        else:
            brain.card_to_follow(Player,suit_led);

def setup():
    global deck
    global cards_on_table
    global user_player
    global player1
    global player2
    global player3
    global player4
    global first_hand
    global turn_order

    user_player = gui.single_player

    print len(values)
    print len(suits)
    deck_build()
    random.shuffle(deck)
    print(len(deck))

    first_hand = True
    cards_on_table = []

    player1 = make_player(deck[0:13], 1,1)
    player2 = make_player(deck[13:26],2,2)
    player3 = make_player(deck[26:39],3,3)
    player4 = make_player(deck[39:52],4,4)
    turn_order = [player1,player2,player3,player4]

    lead = find_Card(make_card("2","Clubs"))
    if lead == 1:
        pass
    elif lead == 2:
        player1.turn_pos = 4
        player2.turn_pos = 1
        player3.turn_pos = 2
        player4.turn_pos = 3
        turn_order = [player2,player3,player4,player1]
    elif lead == 3:
        player1.turn_pos = 3
        player2.turn_pos = 4
        player3.turn_pos = 1
        player4.turn_pos = 2
        turn_order = [player3,player4,player1,player2]
    else:
        player1.turn_pos = 2
        player2.turn_pos = 3
        player3.turn_pos = 4
        player4.turn_pos = 1
        turn_order = [player4,player1,player2,player3]

    player1.print_hand()
    player2.print_hand()
    player3.print_hand()
    player4.print_hand()

def NextPlay():
    global player1
    global player2
    global player3
    global player4
    global suit_led
    global turn_order
    global user_player
    global cards_on_table
    global already_played
    global user_card_selected

    if len(deck) == 0:
        gui.app.stats_window()

    if len(cards_on_table) == 4:
        cards_on_table = []
        gui.app.reset_cards()

    for x in turn_order:
        gui.p.set("Player Leading: " + str(turn_order[0].name));

        if x.name == 1 and user_player:
            var = Tkinter.StringVar()
            ls = [y.name + " of " + y.suit for y in player1.Hand]
            var.set("Choose Card")
            z = Tkinter.OptionMenu(gui.app, var, *ls).grid(column=0,row=5)

            ready = Tkinter.Button(gui.app,text="Selected!", command=change_ready)
            ready.grid(column=1,row=5)

            wait = raw_input("Ready?")

            temp = var.get().split(" ")
            gui.card_chosen = make_card(temp[0],temp[2])

            if not fair_play(gui.card_chosen):

                wait = raw_input("Not Valid Play?")
                temp = var.get().split(" ")
                gui.card_chosen = make_card(temp[0],temp[2])

        play(x,gui.card_chosen,user_player)
        gui.app.update_image(cards_on_table[-1][1],cards_on_table[-1][0])
        if len(cards_on_table) == 4:
            gui.app.update_points()

def change_ready():
    global user_card_selected
    user_card_selected = True

def suits_in_hand(card):
    if card.suit == "Clubs":
        return setup.player1.Clubs
    elif card.suit == "Spades":
        return setup.player1.Spades
    elif card.suit == "Hearts":
        return setup.player1.Hearts
    else:
        return setup.player1.Diamonds

def fair_play(card_played):
    if card_played.suit == suit_led or len(suits_in_hand(card_played)):
        return True
    else:
        return False
