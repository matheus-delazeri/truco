from truco.arguments import exec_args

if __name__ == '__main__':
    from truco.game import Game
    from truco.data.analyser import Analyser

    if exec_args.analyser:
        analyser = Analyser()
        print(analyser)
        analyser.menu()
    else:
        Game(num_players=exec_args.num_players, num_bots=exec_args.num_bots)

