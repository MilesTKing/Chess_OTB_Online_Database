from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)
DATA_ROOT = Path('../../data/raw')
MAX_FILE_SIZE = 1000000  # 1MB for example run.

def reduce_file(infile: Path, outfile: Path, max_size: int):
    file_size = 0
    current_game = []

    with open(infile, 'r') as infile, open(outfile, 'w') as outfile:
        try:
            for line in infile:
                # All pgn games begin with [Event by definition, so it's used as game delimiter
                if '[Event' in line:
                    if current_game:
                        game_str = ''.join(current_game)
                        game_bytes = len(game_str.encode('utf-8'))
    
                        if file_size + game_bytes > max_size:
                            break
    
                        outfile.write(game_str)
                        file_size += game_bytes
                        current_game = []
    
                current_game.append(line)
        except UnicodeDecodeError as e:
            logger.warning(f"Uploading {infile} failed due to decode error")
        except Exception as e:
            logger.warning(f"Uploading {infile} failed: {e}")
            return

        # Write game
        if current_game:
            game_str = ''.join(current_game)
            game_bytes = len(game_str.encode('utf-8'))

            if file_size + game_bytes <= max_size:
                outfile.write(game_str)


def process_all_files():
    # Gets all pgn files
    for file in DATA_ROOT.rglob("*.pgn"):
        print(f"Reducing {file}")
        size = os.path.getsize(file)

        # Skips reduced files
        if file.stem.endswith("_reduced"):
            continue

        # Skips files under 10GB
        if size <= MAX_FILE_SIZE:
            print(f"Skipping file: {file}")
            continue

        output_file = file.with_name(f"{file.stem}_reduced.pgn")
        reduce_file(file, output_file, MAX_FILE_SIZE)
process_all_files()
print("Done.")