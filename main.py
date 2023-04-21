import argparse

parser = argparse.ArgumentParser("main.py")
parser.add_argument("-b", dest="num_bots", default="1", type=int, help="Number of bots")
parser.add_argument("-p", dest="num_players", default="1", type=int, help="Number of players")
parser.add_argument("-d", "--debbuger", action="store_true", help="Enable debbuger")
exec_args = parser.parse_args()

if __name__ == '__main__':
    from truco.game import Game
    Game(num_players=exec_args.num_players, num_bots=exec_args.num_bots)

