from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["chess"]
collection = db["games"]

count = collection.count_documents({})
print(f"Total games in DB: {count}")

print("\nSample games:")
for doc in collection.find().limit(5):
    print(doc)

print("\nGames with > 50 moves:")
for doc in collection.find({"Move_Count": {"$gt": 50}}).limit(5):
    print(doc)

print("\nGames with White Elo > 2000:")
for doc in collection.find({"White_Elo": {"$gt": 2000}}).limit(5):
    print(doc)

print("\nFIDE games:")
for doc in collection.find({"rating_type": "fide"}).limit(5):
    print(doc)

client.close()