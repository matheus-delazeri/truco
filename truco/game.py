from truco.deck import Deck
from truco.player import Player, Bot
from random import shuffle


class Game:
    winner = False

    def __init__(self, num_players=1, num_bots=1):
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

            def __init__(self, index: int, plays=None):
                if plays is None:
                    plays = list()
                self.plays = plays
                self.index = index

            # Get player's plays available
            def get_plays_available(self, player: Player):
                plays_available = ["fold"]
                for card in player.cards:
                    plays_available.append(f"{card.number} of {card.get_suit_label()}")
                if self.index == 0:
                    if self.call_in_progress is None:
                        plays_available.extend(["envido", "truco"])
                    else:
                        plays_available.extend(
                            [f"Decline {self.call_in_progress.play}", f"Accept {self.call_in_progress.play}"])

                return dict(zip(range(len(plays_available)), plays_available))

            def save_play(self, play, player: Player):
                new_play = self.Play(play, player)
                self.plays.append(new_play)
                if new_play.type == "call":
                    self.call_in_progress = new_play

                return new_play

            def calc_results(self):
                pass

            class Play:
                class Points:
                    CALLS = {
                        "envido": 2,
                        "real_envido": 5,
                        "truco": 2,
                        "retruco": 3,
                        "vale_quatro": 4,
                        "flor": 3,
                        "contra_flor": 6
                    }

                accepted = False
                value = 0
                player_winner = None

                def __init__(self, play, player: Player):
                    self.player = player
                    self.play = play
                    if play in self.Points.CALLS:
                        self.type = "call"
                        self.value = self.Points.CALLS[play]
                    elif play == "fold":
                        self.type = "fold"
                    else:
                        self.type = "card"

                def print(self):
                    if self.type == "call":
                        print(f"{self.player.name} called {self.play}")
                    elif self.type == "card":
                        print(f"{self.player.name} plays {self.play}")
                    elif self.type == "fold":
                        print(f"{self.player.name} fold")
