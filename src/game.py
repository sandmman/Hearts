import player
import card
import random
import Tkinter
import brain
import gui


class Game(object):
    def __init__(self):
        self.already_played = []
        self.cards_on_table = []
        self.turn_order = []
        self.suit_led = "Clubs"
        self.first_hand = True
        self.user_player = False

        self.player1 = player.make_player([],1,1)
        self.player2 = player.make_player([],2,2)
        self.player3 = player.make_player([],3,3)
        self.player4 = player.make_player([],4,4)

        self.deck = []
        self.clubs  = []
        self.spades = []
        self.hearts = []
        self.diamonds = []

        self.turn = 0

    def check(self):
        # Edge case of user player has 2 of clubs
        if self.turn_order[0] == self.player1 and game_type:
            game.first_hand = False

    def who_won_the_trick(self):
        """
            Finds the person who won the trick --- highest card of the led suit
            returns that player
        """
        #[(player,card_played)]
        same_suit = [x for x in self.cards_on_table if x[1].suit == self.cards_on_table[0][1].suit]
        if len(same_suit) == 1:
            return same_suit[0][0]
        # Otherwise sort to find the winner
        same_suit = sorted(same_suit,key=lambda x : (x[1].value),reverse = True)
        return same_suit[0][0]

    def get_next_turn_order(self):
        """
            Gets the order for the next turn based on the current hand
            - Finds the person who wins the trick --- high card of the led suit
            - updates information for the next turn
        """
        self.turn_order = [self.who_won_the_trick()]
        if self.turn_order[0].name == 1:
            self.turn_order = [self.player1,self.player2,self.player3,self.player4]
            self.player1.Points = self.player1.Points + self.points_on_table()
            self.player1.turn_pos = 1
            self.player2.turn_pos = 2
            self.player3.turn_pos = 3
            self.player4.turn_pos = 4
        elif self.turn_order[0].name == 2:
            self.turn_order = [self.player2,self.player3,self.player4,self.player1]
            self.player2.Points = self.player2.Points + self.points_on_table()
            self.player1.turn_pos = 4
            self.player2.turn_pos = 1
            self.player3.turn_pos = 2
            self.player4.turn_pos = 3
        elif self.turn_order[0].name == 3:
            self.turn_order = [self.player3,self.player4,self.player1,self.player2]
            self.player3.Points = self.player3.Points + self.points_on_table()
            self.player1.turn_pos = 3
            self.player2.turn_pos = 4
            self.player3.turn_pos = 1
            self.player4.turn_pos = 2
        else:
            self.turn_order = [self.player4,self.player1,self.player2,self.player3]
            self.player4.Points = self.player4.Points + self.points_on_table()
            self.player1.turn_pos = 2
            self.player2.turn_pos = 3
            self.player3.turn_pos = 4
            self.player4.turn_pos = 1

    def points_on_table(self):
        """
            Calculates the total number of points on a given hand
        """
        points = 0
        point_cards = [x[1] for x in self.cards_on_table if x[1].suit == "Hearts" or (x[1].suit == "Spades" and x[1].name == "Queen")]
        for card in point_cards:
            if card.suit == "Hearts":
                points += 1
            else:
                points += 13

        return points

    def bundler(self,Player,card_played):
        """
            Groups together function calls for each play
        """
        if Player.turn_pos == 1:
            self.suit_led = card_played.suit
            self.card_played = card_played

        self.cards_on_table.append((Player,card_played))
        self.update_player(card_played,Player.name)
        self.update_game_cards(card_played)

        if len(self.cards_on_table) == 4:
            self.get_next_turn_order()
            card.deck_stats(self.deck)
            gui.app.update_points()
            self.turn = -1

    def remove_card_from_player(self,player,card_played):
        """
            Removes recently played card from palyer object
        """
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

    def update_player(self,card_played, name):
        """
            Facilitates the removal of recently played card from player object
            by finding the player and calling remove_card_from_player()
        """
        if name == 1:
            self.player1 = self.remove_card_from_player(self.player1,card_played)
        elif name == 2:
            self.player2 = self.remove_card_from_player(self.player2,card_played)
        elif name == 3:
            self.player3 = self.remove_card_from_player(self.player3,card_played)
        else:
            self.player4 = self.remove_card_from_player(self.player4,card_played)

    def update_game_cards(self,card_played):
        """
            Removes the most recently played cards from the deck
            and from the individual suit arrays
        """
        self.deck = [card for card in self.deck if not card.equals(card_played)]

        if card_played.suit == "Clubs":
            self.clubs.remove(self.find_in_array(card_played,self.clubs))
        elif card_played.suit == "Spades":
            self.spades.remove(self.find_in_array(card_played,self.spades))
        elif card_played.suit == "Diamonds":
            self.diamonds.remove(self.find_in_array(card_played,self.diamonds))
        else:
            self.hearts.remove(self.find_in_array(card_played,self.hearts))

    def NextPlay(self):
        """
            Facilitates a Turn
            Acts as the mediator between the gui class and the backend
        """
        # Check if round is over
        if len(self.deck) == 0:
            gui.app.stats_window()

        # Check if hand is over
        if len(self.cards_on_table) == 4:
            self.cards_on_table = []
            gui.app.reset_cards()

        # Run through the hand
        for x in self.turn_order:
            self.play(x,gui.app.card_chosen)
            gui.app.update_image(self.cards_on_table[-1][1],self.cards_on_table[-1][0])

    def find_Card(self,card):
        """
            Finds a specific card accross all players
            returns the player.name
        """
        for player in self.turn_order:
            for c in player.Hand:
                if c.equals(card):
                    return player.name
        return None

    def find_in_array(self,card_played,array):
        """
            Finds a card object in a given array
        """
        for card in array:
            if card.equals(card_played):
                return card
        return None

    def play(self,Player,card_played):
        """
            Facilitates an individual player's turn
        """
        # Check Round Over
        if len(self.deck) == 0:
            print "Game Over"
        # User Player Turn
        if self.user_player and Player.name == 1:
            if Player.turn_pos == 1:
                self.bundler(Player,card_played)
                first_hand = False
            else:
                self.bundler(Player,card_played)
        # Computer Turn
        else:
            # First Hand must lead 2 of Clubs
            if self.first_hand:
                self.bundler(Player,card.make_card("2","Clubs"))
                self.first_hand = False
            # CPU Player is leading
            elif Player.turn_pos == 1:
                brain.card_to_lead(Player)
                gui.app.p.set("Player " + str(self.turn_order[0].name) + " Led " + self.suit_led);
            # CPU Must follow suit
            else:
                brain.card_to_follow(Player,self.suit_led);
