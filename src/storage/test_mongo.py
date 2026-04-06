from pymongo import MongoClient

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
for doc in collection.find({"rating_type": "otb"}).limit(5):
    print(doc)

client.close()