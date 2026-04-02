import chess.pgn as chess
from pathlib import Path
import time
file_stats = Path('../../data/raw/reduced_lichess.pgn').stat()
file_size = 0
games_buffer = []
start_time = time.perf_counter()
max_file_size = 1000000000
games_finished = False
with open('../../data/raw/lichess.pgn') as lichess_file, open('../../data/raw/reduced_lichess.pgn', 'w') as outfile:
        while file_size < max_file_size and not games_finished:
            for x in range(50000):
                game = chess.read_game(lichess_file)
                if game is None:
                    games_finished = False
                    break
                games_buffer.append(str(game))
            chunk = "".join(games_buffer)
            outfile.write(chunk)
            file_size = Path('../../data/raw/reduced_lichess.pgn').stat().st_size
            print(file_size)
            games_buffer.clear()
            print(f"Time: {time.perf_counter() - start_time} seconds")