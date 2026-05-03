from pymongo import MongoClient
def print_pgn(doc):
    if not doc:
        print("No game found.")
        return

    # Header tags
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

client = MongoClient("mongodb://localhost:27017")

db = client["chess"]
collection = db["games"]

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
for doc in collection.find({"White_Elo": {"$gt": 2000}}).limit(5):
    print(doc)
    
print("\n5 Over the board games:")
for doc in collection.find({"Rating_Type": "otb"}).limit(5):
    print(doc)
print("\n5 Games where Time Control is not None:")
for doc in collection.find({"Time_Control": {"$ne": None}}).limit(5):
    print(doc)
print("Mock game:")
for game in collection.find({
    "White_Player": "Carrasco Rodriguez, Hector",
}):
    print_pgn(game)


client.close()