from pymongo import MongoClient

# Connect to MongoDB (local machine → docker container)
client = MongoClient("mongodb://localhost:27017")

# Database and collection
db = client["chess"]
collection = db["games"]

# -------------------------------
# 1. Count documents
# -------------------------------
count = collection.count_documents({})
print(f"Total games in DB: {count}")

# -------------------------------
# 2. Get sample documents
# -------------------------------
print("\nSample games:")
for doc in collection.find().limit(5):
    print(doc)

# -------------------------------
# 3. Query: games with > 50 moves
# -------------------------------
print("\nGames with > 50 moves:")
for doc in collection.find({"Move_Count": {"$gt": 50}}).limit(5):
    print(doc)

# -------------------------------
# 4. Query: rating range
# -------------------------------
print("\nGames with White Elo > 2000:")
for doc in collection.find({"White_Elo": {"$gt": 2000}}).limit(5):
    print(doc)

# -------------------------------
# 5. Query: by rating type
# -------------------------------
print("\nFIDE games:")
for doc in collection.find({"rating_type": "fide"}).limit(5):
    print(doc)

client.close()