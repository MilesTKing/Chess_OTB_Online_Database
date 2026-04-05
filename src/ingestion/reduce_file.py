from pathlib import Path
import time
lichess_file = Path('../../data/raw/pgn/reduced_lichess.pgn')
reduced_file = Path('../../data/raw/pgn/super_reduced_lichess.pgn')


max_file_size = 10000000
file_size = 0
current_game = []
games_written = 0

with open(lichess_file, 'r', encoding='utf-8') as infile, \
        open(reduced_file, 'w', encoding='utf-8') as outfile:

    for line in infile:
        if '[Event' in line:
            # If we already have a game buffered, write it
            if current_game:
                event = line.partition('[Event')[1]
                event_details = line.partition('[Event')[2]
                event = event + event_details
                current_game.append(line.split('[Event')[0])
                game_str = ''.join(current_game)
                # Stop if writing would exceed max size
                if file_size + len(game_str.encode('utf-8')) > max_file_size:
                    break

                outfile.write(game_str)
                file_size += len(game_str.encode('utf-8'))
                games_written += 1

                current_game = [event]
                line = ''
        if line != '':
            current_game.append(line)

    # Write last game if needed
    if current_game and file_size < max_file_size:
        game_str = ''.join(current_game)
        if file_size + len(game_str.encode('utf-8')) <= max_file_size:
            outfile.write(game_str)