import chess.pgn as chess
with open('../../data/raw/lichess.pgn') as lichess_file:
    with open('../../data/raw/reduced_lichess.pgn', 'w') as outfile:
        
        for line in range(1000):
            game = chess.read_game(lichess_file)
            outfile.write(str(game))
            outfile.write('\n')