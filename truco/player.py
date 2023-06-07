import random
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from os import path
from truco.log import log
from truco.deck import Deck

class Player:
    NAME_PREFIX = "Player"

    AGENT_PREFIX = "self"
    OPPONENT_PREFIX = "opponent"
    cards = list()

    def __init__(self, number):
        self.name = f"{self.NAME_PREFIX} {number}"
        self.game_knowlodge = {}

    def set_cards(self, cards: list):
        # Sort cards by value, from lowest to higher. 
        # E.g. self.cards[0] = lowest card
        self.cards = Deck.sort_cards_by_value(cards=cards)
        return self

    def choose_play(self, _round):
        plays_available = _round.get_plays_available(self)
        print("[GAME] Plays available: \n")
        for _, option in plays_available.items():
            id, msg = option
            print(f" [{id}] - {msg.title()}")
        return int(input(f"\n[GAME] {self.name}, what you want to do: "))


    def store_knowlodge(self, file="stored_knowlodge.csv"):
        file_path = path.join(path.dirname(__file__), file)
        df = pd.DataFrame(data=self.get_game_knowlodge(), index=list(self.get_game_knowlodge().keys()))
        if path.isfile(file_path):
            old_df = pd.read_csv(file_path)    
            df = pd.concat([df, old_df], ignore_index=True)

        df.to_csv(file_path, index=False)

    @log
    def get_game_knowlodge(self):
        return self.game_knowlodge

    def save_round_knowlodge(self, _round):
        # Get all non-played cards and add its respective column
        # to the `hand_data` that will be then used to find the 
        # nearest neighbor

        # Use already played cards from opponent as input 
        for play in _round.plays:
            if play.type == "card" and play.player is not self:
                attribute = f"{self.OPPONENT_PREFIX}_round_{_round.index}"
            elif play.player is self:
                attribute = f"{self.AGENT_PREFIX}_round_{_round.index}"

            for index, card in enumerate(play.player.cards):
                if card.played:
                    if index == 0:
                        card_index = 9
                    elif index == 1:
                        card_index = 10
                    elif index == 2:
                        card_index = 11

            self.game_knowlodge[attribute] = card_index

class Bot(Player):
    NAME_PREFIX = "Bot"

    NUM_NEIGHBORS = 5

    def __init__(self, number):
        super().__init__(number)
        self.name = f"{self.NAME_PREFIX} {number}"
        self.cases_path = path.join(path.dirname(__file__), "data", "no_fold.csv")
        self.df = pd.read_csv(self.cases_path, header=0).dropna()

    def set_cards(self, cards: list):
        super().set_cards(cards)
        for index, card in enumerate(self.cards):
            attribute = f"{self.AGENT_PREFIX}_"
            if index ==   0: attribute += "low_card"
            elif index == 1: attribute += "medium_card"
            elif index == 2: attribute += "high_card"

            self.game_knowlodge[attribute] = card.get_value()

        return self


    def choose_play(self, _round):
        option_id = int(self.calculate_play(_round))

        return option_id if option_id in [option[0] for _, option in _round.get_plays_available(self).items()] else 8

    @log
    # Only handles card plays for now
    def calculate_play(self, _round):
        game_knowlodge = self.get_game_knowlodge()
        round_label = f"{self.AGENT_PREFIX}_round_{_round.index}"
        attributes = self.df[list(game_knowlodge.keys())]
        label = self.df[round_label]

        kNeighborsClassifier = KNeighborsClassifier(n_neighbors=self.NUM_NEIGHBORS).fit(attributes, label)

        hand_cards_df = pd.DataFrame(data=game_knowlodge, index=list(game_knowlodge.keys()))
        predicted_values = kNeighborsClassifier.predict(X=hand_cards_df)
        return int(predicted_values[0])


    @log
    def get_nearest_neighbor(self, kNeighborsClassifier: KNeighborsClassifier, _case: pd.DataFrame):
        neighbor_row = kNeighborsClassifier.kneighbors(_case, n_neighbors=1)[1][0].item()
        return self.df.loc[neighbor_row]


