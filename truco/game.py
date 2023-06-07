from enum import Enum
from truco.deck import Deck
from truco.player import Player, Bot
from random import shuffle
from functools import reduce
from collections import Counter

from truco.log import log

class Game:
    winner = False

    def __init__(self, num_players=1, num_bots=1):
        print("\n------ GAME ------\n")
        self.players = [Player(n) for n in range(num_players)] + [Bot(n) for n in range(num_bots)]
        shuffle(self.players)  # Random order players
        #while not self.winner:
        hand = self.Hand(self.players)
        self.update_play_order()

        for player in hand.players:
            player.store_knowlodge()


    # Move players 1 position to 'right', making the new first player the hand
    def update_play_order(self):
        self.players.insert(0, self.players.pop())

    class Hand:
        NUM_ROUNDS = 3
        winner = None

        def __init__(self, players):
            self.deck = Deck()
            self.players = [player.set_cards(self.deck.draw_cards(amount=3)) for player in players]
            self.rounds = [self.Round(n) for n in range(self.NUM_ROUNDS)]
            # An exit call can be a Truco decline or a fold
            exit_call = False
            for _round in self.rounds:
                for player in self.players:
                    play = False
                    while not play:
                       chosen_play = player.choose_play(_round)
                       play = _round.save_play(chosen_play, player)

                    print(play)
                    if play.type == "card":
                        if chosen_play == self.Round.Play.Options.LOW_CARD.value:
                            card_index = 0
                        elif chosen_play == self.Round.Play.Options.MEDIUM_CARD.value:
                            card_index = 1
                        else:
                            card_index = 2

                        player.cards[card_index].played = True
                    elif play.type == "call":
                        if play.id == self.Round.Play.Options.FOLD.value:
                            exit_call = True
                            break
                        play.accepted = int(input(f"[GAME] Accept it? (1 or 0): ")) == 1
                        if play.id == self.Round.Play.Options.TRUCO.value and not play.accepted:
                           exit_call = True
                           break

                _round.calc_results(self.players)
                print(f"[GAME] Round {_round.index} winner: {_round.winner.name}")
                if _round.index == 1 and (self.rounds[0].winner == _round.winner):
                    break

                for index, player in enumerate(self.players):
                    player.save_round_knowlodge(_round)
                    if player is _round.winner:
                        self.players.insert(0, self.players.pop(index))
                        break

                if exit_call:
                    break

            self.winner = self.get_winner()
            print(f"[GAME] Hand winner: {self.winner.name}")

        @log
        def get_winner(self):
            counter = Counter([_round.winner for _round in self.rounds if _round.winner is not None])
            most_common = counter.most_common(1)
            return most_common[0][0] if most_common else None
 

        class Round:
            call_in_progress = None
            winner = None
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
            
                plays_available.append((play_options.TRUCO.value, play_options.TRUCO.name))
                if self.index == 0: 
                    plays_available.append((play_options.ENVIDO.value, play_options.ENVIDO.name))

                return dict(zip(range(len(plays_available)), plays_available))

            def save_play(self, play_id, player: Player):
                new_play = self.Play(play_id, player)
                if not new_play.type:
                    print("[GAME] Invalid play index. Try again")
                    return False

                self.plays.append(new_play)
                if new_play.type == "call":
                    self.call_in_progress = new_play

                return new_play

            def calc_results(self, players: list):
                call_plays = [play for play in self.plays if play.type == "call"]
                for play in call_plays:
                    if play.id == self.Play.Options.FOLD.value:
                        self.winner = [player for player in players if player != play.player][0]
                        return self.winner

                card_plays = [play for play in self.plays if play.type == "card"]
                if card_plays:
                    # Get biggest card played
                    winner_play = reduce(
                            lambda p1, p2: p1 if (p1.get_played_card().get_value() > p2.get_played_card().get_value()) else p2, 
                            card_plays)
                    self.winner = winner_play.player

                return self.winner


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

                type = False
                accepted = False
                value = 0

                def __init__(self, play_id, player: Player):
                    self.id = play_id
                    self.player = player
                    if self.id in self.CALLS:
                        self.key = self.CALLS[self.id]["key"]
                        self.type = "call"
                        self.value = self.CALLS[self.id]["value"]
                    elif self.id in self.CARDS:
                        self.key = self.CARDS[self.id]["key"]
                        self.type = "card"
                    
                def __str__(self):
                    if self.type == "call":
                        return f"[GAME] {self.player.name} called {self.key}"
                    elif self.type == "card":
                        return f"[GAME] {self.player.name} plays {self.get_played_card()}"
               
                def get_played_card(self):
                    """
                    * Probably not the best way to do it
                    """
                    if (self.type == "card"):
                        card_type_map = {
                                "low_card": 0,
                                "medium_card": 1,
                                "high_card": 2
                        }

                        return self.player.cards[card_type_map[self.key]]

                    return False

