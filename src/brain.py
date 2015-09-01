"""
This module is where all the cpu decision making takes place
"""
import card
import player
import configure


"""
Card Choice Functions

"""

def card_to_throwaway(Player):
    """
    Each CPU plays very defensively:
        1. Throw away the queen of spades
        2. Throw away Highest Heart
        3. Throw card with highest prob of winning the next hand
    """
    queen_of_spades = card.make_card("Queen","Spades")
    if queen_of_spades in Player.Spades:
        return queen_of_spades
    elif len(Player.Hearts) > 0:
        return Player.max_card("Hearts")
    else:
        return probabilities_of_winning_trick(Player.Hand)[-1][0]

def card_to_lead(Player):
    """
        Goal is to not take any tricks so...
        Going to lead the lowest card in hand where
        there are other higher cards out
    """
    card = probabilities_of_winning_trick(Player.Hand)[0][0]
    configure.game.bundler(Player, card)

def card_to_follow(Player,lead):
    """
        Goal is to not take any tricks with Points!
        will play the card with the least likelihood
        of taking points unless you can take it without
        getting points
    """
    possible_plays = get_cards_of_suit(Player,lead)

    if len(possible_plays) > 0:

        probs = probabilities_of_winning_trick(possible_plays)
        probs_for_next_hand = probabilities_of_winning_trick(Player.Hand)

        # If you go last, won't get points, and have low prob of winning next hand
        # --> play highest card of suit
        if (Player.turn_pos == 4 and
            configure.game.points_on_table() == 0 and
            probs_for_next_hand[0][1] < 0.4):
            configure.game.bundler(Player,probs[-1][0]);
        else:
            configure.game.bundler(Player,probs[0][0]);
    #Player can throw away cards of another suit
    else:
        configure.game.bundler(Player,card_to_throwaway(Player))


"""Probability Functions"""
def probability_of_shooting_the_moon():
    return

def probabilities_of_winning_trick(hand):
    """
    Gives the card with the least probability of winning (Simple Algorithm)
       - Meaning the lowest card in a suit with many higher
         cards not in your hand
    """
    probs = []
    for x in hand:
        n = 0;
        if x.suit == "Clubs":
            n = num_cards_lower(hand,x,configure.game.clubs)
            y = num_cards_you_dont_have_in_suit(hand,configure.game.clubs)
        elif x.suit == "Spades":
            n = num_cards_lower(hand,x,configure.game.spades)
            y = num_cards_you_dont_have_in_suit(hand,configure.game.spades)
        elif x.suit == "Diamonds":
            n = num_cards_lower(hand,x,configure.game.diamonds)
            y = num_cards_you_dont_have_in_suit(hand,configure.game.diamonds)
        else:
            n = num_cards_lower(hand,x,configure.game.hearts)
            y = num_cards_you_dont_have_in_suit(hand,configure.game.hearts)
        if y == 0:
            y = 1
        probs.append((x,float(n)/y))
    return sorted(probs,key=lambda x : x[1])

"""
gui Functions
"""
def get_cards_of_suit(Player,suit):
    if suit == "Clubs":
        return Player.Clubs
    elif suit == "Spades":
        return Player.Spades
    elif suit == "Hearts":
        return Player.Hearts
    else:
        return Player.Diamonds

def search(hand,card):
    # Return true if card is in the players hand
    for x in hand:
        if x.equals(card):
            return True
    return False

def num_cards_lower(hand,card,array):
    n = 0
    for x in array:
        if x.value < card.value and not search(hand,x):
            n += 1
    return n

def num_cards_you_dont_have_in_suit(hand,array_of_suit):
    n = 0
    for card in array_of_suit:
        if not search(hand,card):
            n += 1
    return n
