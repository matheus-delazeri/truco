from random import shuffle


class Deck:
    def __init__(self):
        self.deck = [self.Card(n, suit) for suit in range(1, 5) for n in range(1, 13) if n < 8 or n >= 10]
        shuffle(self.deck)

    def draw_cards(self, amount=1):
        cards, self.deck = self.deck[:amount], self.deck[amount:]
        return cards


    class Card:
        played = False
        SUIT_LABEL = {
            1: "ESPADAS",
            2: "OUROS",
            3: "COPAS",
            4: "BASTOS"
        }
        class Weights:

            BY_SUIT = {
                1: { 7: 42, 1: 52 }, # 7 e de ESPADAS
                2: { 7: 40 }, # 7 de OUROS
                4: { 1: 50 }, # 1 de BASTOS
            }

            BY_NUMBER = {
                3: 24,
                2: 16,
                1: 12,
                12: 8,
                11: 7,
                10: 6,
                7: 4,
                6: 3,
                5: 2,
                4: 1
            }

        def __init__(self, number: int, suit_id: int):
            self.number = number
            self.suit_id = suit_id

        def get_suit_label(self):
            return self.SUIT_LABEL[self.suit_id]

        # Get card's real value
        def get_value(self):
            if self.suit_id in self.Weights.BY_SUIT:
               suit_weights = self.Weights.BY_SUIT[self.suit_id]
               if self.number in suit_weights:
                   return suit_weights[self.number]

            return self.Weights.BY_NUMBER[self.number]

