from random import shuffle


class Deck:
    def __init__(self):
        self.deck = [Card(n, suit) for suit in range(1, 5) for n in range(1, 13) if n < 8 or n >= 10]
        shuffle(self.deck)

    def draw_cards(self, amount=1):
        cards, self.deck = self.deck[:amount], self.deck[amount:]
        return cards


class Card:
    suit_label = {
        1: "ESPADAS",
        2: "OUROS",
        3: "COPAS",
        4: "BASTOS"
    }

    def __init__(self, number: int, suit_id: int):
        self.number = number
        self.suit_id = suit_id

    def get_suit_label(self):
        return self.suit_label[self.suit_id]

