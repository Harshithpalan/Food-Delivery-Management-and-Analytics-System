import os
from pymongo import MongoClient
import pymongo
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "food_delivery_db")

@st.cache_resource
def get_database_connection():
    """
    Establish and return a connection to the MongoDB database.
    We use @st.cache_resource to prevent Streamlit from reconnecting on every rerun.
    """
    try:
        # Create a MongoDB client
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Force a call to check if connection is successful
        client.admin.command('ping')
        print("MongoDB connected successfully")
        
        # Get the database instance
        db = client[MONGO_DB_NAME]
        return db, client
        
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        st.error(f"Failed to connect to MongoDB: {e}")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def initialize_indexes(db):
    """
    Initializes necessary MongoDB indexes for performance optimization.
    """
    try:
        # 1. Customers Collection
        # _id is used as customer_id, so it is automatically indexed and unique by default.
        # We index 'phone' because it is frequently used to search for customers.
        db.customers.create_index("phone", unique=True)
        
        # 2. Restaurants Collection
        # _id is used as restaurant_id.
        # We index 'location' because users frequently filter restaurants by city.
        db.restaurants.create_index("location")
        
        # 3. Food Items Collection
        # _id is used as food_id.
        # We index 'restaurant_id' because we frequently fetch all food items for a specific restaurant.
        db.food_items.create_index("restaurant_id")
        
        # 4. Orders Collection
        # _id is used as order_id.
        # We index 'customer_id' to quickly find a customer's order history.
        db.orders.create_index("customer_id")
        # We index 'restaurant_id' for fast aggregation of restaurant revenue and top restaurants.
        db.orders.create_index("restaurant_id")
        # We index 'ordered_at' to efficiently filter orders by date for time-series analytics (e.g., revenue by date).
        db.orders.create_index([("ordered_at", pymongo.DESCENDING)])
        
    except Exception as e:
        print(f"Error initializing indexes: {e}")

def get_all_indexes(db):
    """
    Diagnostic function to retrieve and verify all indexes in the database.
    """
    indexes = {}
    try:
        for collection_name in db.list_collection_names():
            # Get index keys for each collection
            indexes[collection_name] = list(db[collection_name].index_information().keys())
    except Exception as e:
        pass
    return indexes
