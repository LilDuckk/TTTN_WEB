from app import db

class Game:
    def __init__(self):
        self.players = []
        self.properties = []
        self.current_turn = 0
        self.auctions = []
        self.chance_deck = []
        self.community_chest_deck = []

    def roll_dice(self):
        import random
        return random.randint(1, 6), random.randint(1, 6)

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def add_player(self, player):
        self.players.append(player)

    def add_property(self, property_):
        self.properties.append(property_)

    def __repr__(self):
        return f'<Game with {len(self.players)} players>'