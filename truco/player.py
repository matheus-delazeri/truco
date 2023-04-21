import random
from pprint import pprint

from truco.log import log

class Player:
    NAME_PREFIX = "Player"
    cards = list()

    def __init__(self, number):
        self.name = f"{self.NAME_PREFIX} {number}"

    def set_cards(self, cards: list):
        # Sort cards by value, from lowest to higher. 
        # E.g. self.cards[0] = lowest card
        self.cards = sorted(cards, key=lambda obj: obj.get_value())
        return self

    def choose_play(self, _round):
        plays_available = _round.get_plays_available(self)
        print("[GAME] Plays available: \n")
        for _, option in plays_available.items():
            id, msg = option
            print(f" [{id}] - {msg.title()}")
        return int(input("\n[GAME] What you want to do: "))

class Bot(Player):
    NAME_PREFIX = "Bot"

    def __init__(self, number):
        super().__init__(number)
        self.name = f"{self.NAME_PREFIX} {number}"

    def choose_play(self, _round):
        return random.choice(_round.get_plays_available(self))
