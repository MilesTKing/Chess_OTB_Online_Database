from pymongo import MongoClient

def print_pgn(doc):
    if not doc:
        print("No game found.")
        return

    print(f'[Event "{doc.get("Event", "?")}"]')
    print(f'[Site "?"]')
    print(f'[Date "{doc.get("UTC_Date") or "????.??.??"}"]')
    print(f'[Round "{doc.get("Round", "?")}"]')
    print(f'[White "{doc.get("White_Player", "?")}"]')
    print(f'[Black "{doc.get("Black_Player", "?")}"]')
    print(f'[Result "{doc.get("Result", "*")}"]')

    if doc.get("White_Elo") is not None:
        print(f'[WhiteElo "{doc["White_Elo"]}"]')
    if doc.get("Black_Elo") is not None:
        print(f'[BlackElo "{doc["Black_Elo"]}"]')
    if doc.get("ECO"):
        print(f'[ECO "{doc["ECO"]}"]')
    if doc.get("Time_Control"):
        print(f'[TimeControl "{doc["Time_Control"]}"]')

    print()

    moves = doc.get("Moves", [])
    formatted_moves = []
    for i in range(0, len(moves), 2):
        move_num = i // 2 + 1
        white_move = moves[i]
        black_move = moves[i + 1] if i + 1 < len(moves) else ""
        formatted_moves.append(f"{move_num}. {white_move} {black_move}".strip())

    print(" ".join(formatted_moves), doc.get("Result", "*"))
    print("\n" + "="*80 + "\n")


client = MongoClient("mongodb://localhost:27017")

db = client["chess"]
collection = db["games"]

# =========================
# VALIDATION: TRACKED GAMES
# =========================

print("\n===== VALIDATION: SPECIFIC GAME TRACE =====\n")

# 1. Paris 1843
print("Paris 1843 Game:")
doc = collection.find_one({
    "Event": "Paris",
    "White_Player": "Kieseritzky, Lionel",
    "Black_Player": "Saint Amant, Pierre C"
})
print_pgn(doc)

# 2. Sitges 1934
print("Sitges 1934 Game:")
doc = collection.find_one({
    "Event": "Sitges",
    "White_Player": "Sunyer, Julio",
    "Black_Player": "Tartakower, Savielly"
})
print_pgn(doc)

# 3. NCCC APA102 ICCF Game
print("NCCC APA102 Game:")
doc = collection.find_one({
    "Event": "NCCC APA102 (ENG)",
    "White_Player": "Elwood, David",
    "Black_Player": "Mahony, Jon D."
})
print_pgn(doc)

# 4. Pranav vs Svane (Blitz edge case)
print("Pranav vs Svane Game:")
doc = collection.find_one({
    "White_Player": "Pranav, V",
    "Black_Player": "Svane, Frederik"
})
print_pgn(doc)

# 5. Lichess Blitz Game
print("Lichess Blitz Game:")
doc = collection.find_one({
    "White_Player": "eelm_28enpassant",
    "Black_Player": "matsievs",
    "UTC_Date": "2026.01.01"
})
print_pgn(doc)


# =========================
# EXISTING QUERIES (UNCHANGED)
# =========================

count = collection.count_documents({})
print(f"Total games in DB: {count}")

print("\n5 random Games:")
for doc in collection.find().limit(5):
    print(doc)

print("\n5 Games with > 100 moves:")
for doc in collection.find({"Move_Count": {"$gt": 100}}).limit(5):
    print(doc)

print("\n5 Games with White Elo > 2000:")
for doc in collection.find({"White_Elo": {"$gt": 2000}}).limit(5):
    print(doc)

print("\n5 Games with Black Elo < 2000:")
for doc in collection.find({"Black_Elo": {"$lt": 2000}}).limit(5):
    print(doc)

print("\n5 Over the board games:")
for doc in collection.find({"Rating_Type": "otb"}).limit(5):
    print(doc)

print("\n5 Games where Time Control is not None:")
for doc in collection.find({"Time_Control": {"$ne": None}}).limit(5):
    print(doc)


client.close()