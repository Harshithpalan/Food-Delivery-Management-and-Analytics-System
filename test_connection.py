from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

# Load environment variables (fallback to defaults if .env not found)
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "food_delivery_db")

def test_connection():
    print(f"Attempting to connect to: {MONGO_URI}")
    
    try:
        # 1. Connect to MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # 2. Select database
        db = client[MONGO_DB_NAME]
        
        # 3. Ping MongoDB
        client.admin.command("ping")
        
        # 4. Print clear success message
        print("SUCCESS: MongoDB connected successfully")
        print(f"Connected to database: {db.name}")
        
    except ConnectionFailure as e:
        print("ERROR: Failed to connect to MongoDB.")
        print(f"Details: {e}")
    except Exception as e:
        print("ERROR: An unexpected error occurred.")
        print(f"Details: {e}")

if __name__ == "__main__":
    test_connection()
