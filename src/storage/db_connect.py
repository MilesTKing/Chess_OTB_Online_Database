import chess.pgn as chess
import sqlite3

connection = sqlite3.connect('chess_data.db')
cursor = connection.cursor()

headers_to_extract = ['Site', 'Date', 'White', 'Black', 'Result', 'WhiteElo', 'BlackElo','ECO','TimeControl', 'Result','Termination']
with open("../../docs/Mock_data/truncated_lichess_file.pgn") as game_file:
    print("Data storage initiated...")
    for line in range(10):
        game = chess.read_game(game_file)
        headers = game.headers
        values = []
        for header in headers_to_extract:
            values.append(headers[header])
        connection.execute("""
            INSERT INTO games (
            site_id,date,white_id,black_id,white_elo,black_elo,result,termination_condition,time_control,ECO,moves) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """, values)
    connection.commit()
    connection.close()