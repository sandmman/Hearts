class Player(object):
    name = 0
    turn_pos = 0
    Points = 0
    Hand = []
    Clubs = []
    Spades = []
    Hearts = []
    Diamonds = []

    # The class "constructor" - It's actually an initializer
    def __init__(self, hand, name, pos):
        self.name = name
        self.turn_pos = pos
        self.Hand = hand
        self.Clubs = [c for c in hand if c.suit == "Clubs"]
        self.Spades = [c for c in hand if c.suit == "Spades"]
        self.Hearts = [c for c in hand if c.suit == "Hearts"]
        self.Diamonds =[c for c in hand if c.suit == "Diamonds"]
        
    def print_hand(self):
        for x in self.Hand:
            print(x.name + " of " + x.suit)
        print("\n")

    def max_card(self,suit):
        if suit == "Clubs":
            suits = self.Clubs
        elif suit == "Spades":
            suits = self.Spades
        elif suit == "Hearts":
            suits = self.Hearts
        else:
            suits = self.Diamonds
        return sorted(suits,key=lambda x : x.value,reverse = True)[0]

def make_player(hand,num,pos):
    player = Player(hand,num, pos)
    return player
