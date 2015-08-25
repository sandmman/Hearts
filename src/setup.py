from player import *
from card import *
import random
import Tkinter
import string



#Global Variables



player1 = ""
player2 = ""
player3 = ""
player4 = ""

leading = 0
played = []
turn_order = []
suit_led = "Clubs"
first_hand = True



def card_to_throwaway(Player):
    """
    Function for deciding the cpu's throwaway card.
    First it tries to throw away the queen of spades, then throws
    its hearts
    """
    queen_of_spades= make_card("Queen","Spades")
    if queen_of_spades in Player.Spades:
        return queen_of_spades
    elif len(Player.Hearts) > 0:
        return Player.Hearts[0]
    else:
        return Player.max_card()

def get_cards_of_suit(Player,suit):
    if suit == "Clubs":
        return Player.Clubs
    elif suit == "Spades":
        return Player.Spades
    elif suit == "Hearts":
        return Player.Hearts
    else:
        return Player.Diamonds

def get_next_lead():
    global turn_order
    global played
    global leading
    global first_hand
    global player1
    global player2
    global player3
    global player4

    #[(player,card_played)]
    same_suit = [x for x in played if x[1].suit == played[0][1].suit]
    if len(same_suit) == 1:
        turn_order = [x[0] for x in played]
    same_suit = sorted(same_suit,key=lambda x : (x[1].value),reverse = True)

    turn_order = [same_suit[0][0]]
    if turn_order[0].player_num == 1:
        turn_order = [player1,player2,player3,player4]
        player1.turn_pos = 1
        player2.turn_pos = 2
        player3.turn_pos = 3
        player4.turn_pos = 4
    elif turn_order[0].player_num == 2:
        turn_order = [player2,player3,player4,player1]
        player1.turn_pos = 4
        player2.turn_pos = 1
        player3.turn_pos = 2
        player4.turn_pos = 3
    elif turn_order[0].player_num == 3:
        turn_order = [player3,player4,player1,player2]
        player1.turn_pos = 3
        player2.turn_pos = 4
        player3.turn_pos = 1
        player4.turn_pos = 2
    else:
        turn_order = [player4,player1,player2,player3]
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

def update_player(card_played, player_num):
    global player1
    global player2
    global player3
    global player4

    if player_num == 1:
        player1 = remove_card(player1,card_played)
    if player_num == 2:
        player2 = remove_card(player2,card_played)
    if player_num == 3:
        player3 = remove_card(player3,card_played)
    if player_num == 4:
        player4 = remove_card(player4,card_played)

def update_deck(card_played):
    global deck
    deck = [card for card in deck if not card.equals(card_played)]

def helper(Player,card_played,leading):
    global played
    global suit_led

    card_played.print_card(Player)
    played.append((Player,card_played))
    if leading:
        suit_led = card_played.suit
    update_player(card_played,Player.player_num)
    update_deck(card_played)

def find_Card(card):
    global turn_order

    for player in turn_order:
        for c in player.Hand:
            if c.equals(card):
                return player.player_num
    return 0

def play(Player):
    global turn_order
    global played
    global leading
    global first_hand
    global player1
    global player2
    global player3
    global player4

    if first_hand:
        helper(Player,make_card("2","Clubs"),True)
        first_hand = False
        leading = Player.player_num
    #Player is leading
    else:
        if Player.turn_pos == 1:
            leading = Player.player_num
            helper(Player,Player.Hand[0],True)

        #Player has to follow suit, if possible
        else:
            #Player has a card of the same suit
            possible_plays = get_cards_of_suit(Player,suit_led)
            if len(possible_plays) > 0:
                helper(Player,possible_plays[0],False)

            #Player can throw away cards of another suit
            else:
                helper(Player,card_to_throwaway(Player),False)

def setup():
    global deck
    global turn_order
    global played
    global leading
    global first_hand
    global player1
    global player2
    global player3
    global player4

    deck_build()
    random.shuffle(deck)

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


def run():
    global deck
    global turn_order
    global played

    if len(deck) == 0:
        return True
    else:
        print("Next Play...")
        played = []
        for player in turn_order:
            play(player)
        get_next_lead()
        deck_stats(deck)
        print("\n")
    return False
