import argparse

parser = argparse.ArgumentParser("-m truco")
parser.add_argument("-b", dest="num_bots", default="1", type=int, help="Number of bots")
parser.add_argument("-p", dest="num_players", default="1", type=int, help="Number of players")
parser.add_argument("-d", "--debbuger", action="store_true", help="Enable debbuger")
parser.add_argument("-a", "--analyser", action="store_true", help="Enable case base analyser")
exec_args = parser.parse_args()
