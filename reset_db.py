import os
from pymongo import MongoClient
from dotenv import load_dotenv

def reset_database():
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "food_delivery_db")

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    print(f"Connecting to MongoDB at {MONGO_URI}...")
    
    db.customers.drop()
    print("- Dropped 'customers' collection")
    
    db.restaurants.drop()
    print("- Dropped 'restaurants' collection")
    
    db.food_items.drop()
    print("- Dropped 'food_items' collection")
    
    db.orders.drop()
    print("- Dropped 'orders' collection")

    print("\nDatabase has been completely reset. It is now empty and ready for new data!")

if __name__ == "__main__":
    reset_database()
