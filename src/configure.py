import player
import card
import random
import game as g

game = ""

def setup(game_type):
    """ Initializes the game and sets up decks/players """
    global game
    game = g.Game()

    game.user_player = game_type
    cards = card.deck_build()
    random.shuffle(cards[0])

    game.deck = cards[0]
    game.clubs = cards[1]
    game.spades = cards[2]
    game.diamonds = cards[3]
    game.hearts = cards[4]

    game.player1 = player.make_player(game.deck[0:13], 1,1)
    game.player2 = player.make_player(game.deck[13:26],2,2)
    game.player3 = player.make_player(game.deck[26:39],3,3)
    game.player4 = player.make_player(game.deck[39:52],4,4)
    game.turn_order = [game.player1,game.player2,game.player3,game.player4]

    c = card.make_card("2","Clubs")

    lead = game.find_Card(c)
    if lead == 1:
        pass
    elif lead == 2:
        game.player1.turn_pos = 4
        game.player2.turn_pos = 1
        game.player3.turn_pos = 2
        game.player4.turn_pos = 3
        game.turn_order = [game.player2,game.player3,game.player4,game.player1]
    elif lead == 3:
        game.player1.turn_pos = 3
        game.player2.turn_pos = 4
        game.player3.turn_pos = 1
        game.player4.turn_pos = 2
        game.turn_order = [game.player3,game.player4,game.player1,game.player2]
    else:
        game.player1.turn_pos = 2
        game.player2.turn_pos = 3
        game.player3.turn_pos = 4
        game.player4.turn_pos = 1
        game.turn_order = [game.player4,game.player1,game.player2,game.player3]

    game.player1.print_hand()
    game.player2.print_hand()
    game.player3.print_hand()
    game.player4.print_hand()

    # Edge case of user player has 2 of clubs
    if game.turn_order[0] == game.player1 and game_type:
        #app.set_disabled()
        game.first_hand = False
