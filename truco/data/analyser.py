import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from os import path
from tabulate import tabulate
import matplotlib.pyplot as plt

from truco.deck import Deck


class Analyser:
    def __init__(self, cases_file="cases.csv"):
        self.cases_path = path.join(path.dirname(__file__), cases_file)
        self.df = pd.read_csv(self.cases_path, header=0)

    def __str__(self):
        file_size = "{}mb".format(
            round(path.getsize(self.cases_path) / pow(1024, 2), 2))
        return "\n---- Analyser ----\n> {}\n\n{}".format(
            "Data analysis of the case dataset used in bot training",
            tabulate(
                [[path.basename(self.cases_path), file_size,
                  self.df.shape[0], self.df.shape[1]]],
                headers=['Cases File', 'File Size', 'N. Cases', 'N. Columns'],
                tablefmt='rounded_outline'
            )
        )

    def free_analysis(self):
        "Compare two columns freely"

        x_axis = input("- Compare column [X axis]: ")
        y_axis = input("- With column [Y axis]: ")

        return self.df[[x_axis, y_axis]]

    def nearest_neighbor_of_hand(self):
        "Get the neighbor hand (most similar) of a given hand"

        values = self.df[
            [
                'self_high_card',
                'self_medium_card',
                'self_low_card',
            ]
        ]
        labels = self.df['self_hand_balance']

        kNeighborsClassifier = KNeighborsClassifier(
            n_neighbors=5).fit(values, labels)

        n_cards = 3
       
        hand_cards = []
        print("\nCARD SUITS MAP\n------------\n")
        for id, label in Deck.Card.SUIT_LABEL.items():
            print("[{}] - {}".format(id, label))
        for i in range(1, n_cards+1):
            card_number = input("\n> Card [{}] number: ".format(i))
            suit_id = input("> Card [{}] suit: ".format(i))
            hand_cards.append(Deck.Card(number=int(card_number), suit_id=int(suit_id)))

        hand_cards = sorted(hand_cards, key=lambda obj: obj.get_value())
        hand_cards_data = {
            'self_high_card': [hand_cards[2].get_value()],
            'self_medium_card': [hand_cards[1].get_value()], 
            'self_low_card': [hand_cards[0].get_value()],
        }
        hand_cards_df = pd.DataFrame(data=hand_cards_data)

        neighbor_row = kNeighborsClassifier.kneighbors(hand_cards_df, n_neighbors=1)[1].item()
        print("\nINPUT HAND\n------------\n")
        print(hand_cards_df.loc[0])
        print("\nNEAREST NEIGHBOR FOUND\n------------\n")
        print(self.df[[
            'id',
            'self_high_card',
            'self_medium_card', 
            'self_low_card',
            'self_hand_balance']].loc[neighbor_row])

        predicted_hand_balance = kNeighborsClassifier.predict(X=hand_cards_df).item()
        print("\n------------\nPREDICTED HAND BALANCE: [{}]".format(predicted_hand_balance))
        print("-- The hand balance predicted for the input hand only using the hand's cards as base")

        return False

    def card_quality_analysis(self):
        "Get a report of the number of hands with a given quality"

        bot_series = pd.Series(self.df["bot_hand_quality"])
        human_series = pd.Series(self.df["human_hand_quality"])
        df = pd.DataFrame()
        df["Quality"] = pd.concat([bot_series, human_series])
        df["Quality"] = df["Quality"].map(
            lambda x:
            "x >= 70" if x >= 70 else ("70 > x >= 30" if x >= 30 and x < 70 else "30 > x >= 0")

        )
        df["Count"] = df.groupby(["Quality"])["Quality"].transform("count")
        df.drop_duplicates(subset=["Quality"], inplace=True)

        return df

    def menu(self):
        method_options = {
            "0": ["Exit", exit],
            "1": ["Free", self.free_analysis],
            "2": ["Card Quality", self.card_quality_analysis],
            "3": ["Nearest Neighbor", self.nearest_neighbor_of_hand],
        }
        print("\n---- Menu ----\n> Choose an analysis method from the list below\n")
        for key in sorted(method_options.keys()):
            method = method_options[key]
            print("[{}]: {}".format(key, method[0]))
            if method[1].__doc__:
                print("-- {}\n".format(method[1].__doc__))

        answer = input("\n> Choose an option: ")
        sub_df = method_options.get(answer, [None, self.menu])[1]()
        if isinstance(sub_df, pd.DataFrame):
            self.Plot().menu(df=sub_df)

        # self.menu()

    class Plot:

        def menu(self, df):
            options = {
                "1": ["Lines graph", self.line_graph],
                "2": ["Scatter graph", self.scatter_graph],
                "3": ["Bar graph", self.bar_graph]
            }
            print("\n> Choose a display method from the list below\n")
            for key in sorted(options.keys()):
                print("[{}]: {}".format(key, options[key][0]))

            answer = input("\n> Choose an option: ")
            options.get(answer, [None, self.menu])[1](df)
            plt.title(f"{df.columns[0]} x {df.columns[1]}")
            plt.xlabel(df.columns[0])
            plt.ylabel(df.columns[1])
            plt.show()

        def line_graph(self, df):
            return plt.plot(df.iloc[:, 0], df.iloc[:, 1])

        def scatter_graph(self, df):
            return plt.scatter(df.iloc[:, 0], df.iloc[:, 1])

        def bar_graph(self, df):
            return plt.bar(df.iloc[:, 0], df.iloc[:, 1])
