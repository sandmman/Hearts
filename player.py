class Player(object):
    player_num = 0
    turn_pos = 0
    points = 0
    Hand = []
    Clubs = []
    Spades = []
    Hearts = []
    Diamonds = []

    # The class "constructor" - It's actually an initializer
    def __init__(self, hand, player_num, pos):
        self.player_num = player_num
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
    def max_card(self):
        return sorted(self.Hand,key=lambda x : x.value,reverse = True)[0]

def make_player(hand,num,pos):
    player = Player(hand,num, pos)
    return player
