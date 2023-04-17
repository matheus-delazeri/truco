import random


class Player:
    NAME_PREFIX = "Player"
    cards = list()

    def __init__(self, number):
        self.name = f"{self.NAME_PREFIX} {number}"

    def set_cards(self, cards: list):
        self.cards = cards
        return self

    def choose_play(self, _round):
        plays_available = _round.get_plays_available(self)
        for i in range(len(plays_available)):
            print(f"[{i}] - {plays_available[i]}")
        play_index = int(input("\n-> What you want to do: "))

        if play_index not in plays_available:
            print("-> Invalid play index, try again...")
            return self.choose_play(_round)

        return plays_available[play_index]


class Bot(Player):
    NAME_PREFIX = "Bot"

    def __init__(self, number):
        super().__init__(number)
        self.name = f"{self.NAME_PREFIX} {number}"

    def choose_play(self, _round):
        return random.choice(_round.get_plays_available(self))
