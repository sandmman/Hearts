import player

deck = []
values = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]
suits = ["Clubs","Spades","Hearts","Diamonds"]

clubs  = []
spades = []
hearts = []
diamonds = []

class Card(object):
    name = ""
    value = 0
    suit = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, name, value, suit):
        self.name = name
        self.value = value
        self.suit = suit
    def equals(self,card):
        if self.name == card.name and self.suit == card.suit:
            return True
        return False
    def print_card(self,Player):
        print("Player" + str(Player.name) + " played: " + self.name  + " of " + self.suit)

def make_card(name, suit):
    card = Card(name, values.index(name), suit)
    return card

def deck_stats(d):

    print("Clubs Remaining:    " + str(len([card for card in d if card.suit == "Clubs"])))
    print("Spades Remaining:   " + str(len([card for card in d if card.suit == "Spades"])))
    print("Hearts Remaining:   " + str(len([card for card in d if card.suit == "Hearts"])))
    print("Diamonds Remaining: " + str(len([card for card in d if card.suit == "Diamonds"])))
    print("\n")

def deck_build():
    global values
    global suits
    global deck

    for x in values:
        for suit in suits:
            card = make_card(x,suit)
            deck.append(card)
            if suit == "Clubs":
                clubs.append(card)
            elif suit == "Spades":
                spades.append(card)
            elif suit == "Diamonds":
                diamonds.append(card)
            else:
                hearts.append(card)
    print "deck size: " + str(len(deck))
