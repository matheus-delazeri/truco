from enum import Enum
from truco.deck import Deck
from truco.player import Player, Bot
from random import shuffle

from truco.log import log

class Game:
    winner = False

    def __init__(self, num_players=1, num_bots=1):
        print("\n------ GAME ------\n")
        self.players = [Player(n) for n in range(num_players)] + [Bot(n) for n in range(num_bots)]
        shuffle(self.players)  # Random order players
        while not self.winner:
            self.Hand(self.players)
            self.update_play_order()

    # Move players 1 position to 'right', making the new first player the hand
    def update_play_order(self):
        self.players.insert(0, self.players.pop())

    class Hand:
        NUM_ROUNDS = 3

        def __init__(self, players):
            self.deck = Deck()
            self.players = [player.set_cards(self.deck.draw_cards(amount=3)) for player in players]
            self.rounds = [self.Round(n) for n in range(self.NUM_ROUNDS)]
            for _round in self.rounds:
                for player in self.players:
                    chosen_play = player.choose_play(_round)
                    _round.save_play(chosen_play, player).print()
                _round.calc_results()

        class Round:
            call_in_progress = None
            player_points = {}

            def __init__(self, index: int, plays=list()):
                self.plays = plays
                self.index = index

            # Get player's plays available
            @log
            def get_plays_available(self, player: Player):
                play_options = self.Play.Options
                plays_available = [(play_options.FOLD.value, play_options.FOLD.name)]
                for index, card in enumerate(player.cards):
                    if not card.played:
                        msg = f"{card.number} of {card.get_suit_label()}"
                        if index == 0:
                            plays_available.append((play_options.LOW_CARD.value, msg))
                        elif index == 1:
                            plays_available.append((play_options.MEDIUM_CARD.value, msg))
                        elif index == 2:
                            plays_available.append((play_options.HIGH_CARD.value, msg))
                
                if self.call_in_progress is None:
                    plays_available.append((play_options.TRUCO.value, play_options.TRUCO.name))
                    if self.index == 0: 
                        plays_available.append((play_options.ENVIDO.value, play_options.ENVIDO.name))
                else:
                    plays_available.append((play_options.DECLINE.value, f"Decline {self.call_in_progress.play_label}"))
                    plays_available.append((play_options.ACCEPT.value, f"Accept {self.call_in_progress.play_label}"))

                return dict(zip(range(len(plays_available)), plays_available))

            def save_play(self, play_id, player: Player):
                new_play = self.Play(play_id, player)
                self.plays.append(new_play)
                if new_play.type == "call":
                    self.call_in_progress = new_play

                return new_play

            def calc_results(self):
                pass

            class Play:
                class Options(Enum):
                    ENVIDO = 1
                    REAL_ENVIDO = 2
                    TRUCO = 3
                    RETRUCO = 4
                    VALE_QUATRO = 5
                    FLOR = 6
                    CONTRA_FLOR = 7
                    FOLD = 8
                    LOW_CARD = 9
                    MEDIUM_CARD = 10
                    HIGH_CARD = 11
                    DECLINE = 12
                    ACCEPT = 13

                CALLS = {
                    Options.ENVIDO.value:      {"value":2,"key":"envido"},
                    Options.REAL_ENVIDO.value: {"value":5,"key":"real_envido"},
                    Options.TRUCO.value:       {"value":2,"key":"truco"},
                    Options.RETRUCO.value:     {"value":3,"key":"retruco"},
                    Options.VALE_QUATRO.value: {"value":4,"key":"vale_quatro"},
                    Options.FLOR.value:        {"value":3,"key":"flor"},
                    Options.CONTRA_FLOR.value: {"value":6,"key":"contra_flor"},
                    Options.FOLD.value:        {"value":0,"key":"fold"},
                }
                CARDS = {
                    Options.LOW_CARD.value:    {"key": "low_card"},
                    Options.MEDIUM_CARD.value: {"key": "medium_card"},
                    Options.HIGH_CARD.value:   {"key": "high_card"}
                }
                ACTIONS = {
                    Options.DECLINE.value:    {"key": "decline"},
                    Options.ACCEPT.value:     {"key": "accept"},
                }

                accepted = False
                value = 0
                player_winner = None

                def __init__(self, play_id, player: Player):
                    self.player = player
                    if play_id in self.CALLS:
                        self.play_label = self.CALLS[play_id]["key"]
                        self.type = "call"
                        self.value = self.CALLS[play_id]["value"]
                    elif play_id in self.CARDS:
                        self.play_label = self.CARDS[play_id]["key"]
                        self.type = "card"
                    else:
                        self.play_label = self.ACTIONS[play_id]["key"]
                        self.type = "action"


                def print(self):
                    if self.type == "call":
                        print(f"[GAME] {self.player.name} called {self.play_label}")
                    elif self.type == "card":
                        print(f"[GAME] {self.player.name} plays {self.play_label}")
                    elif self.type == "fold":
                        print(f"[GAME] {self.player.name} fold")

