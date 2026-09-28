import os
import sys
import random
from datetime import datetime, timedelta

# Add parent directory to path so we can import from database.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_database_connection

def load_sample_data():
    print("Connecting to database...")
    db, client = get_database_connection()
    if db is None:
        print("Failed to connect to database.")
        return

    # 9. Prevent duplicate sample data by dropping collections
    db.customers.drop()
    db.restaurants.drop()
    db.food_items.drop()
    db.orders.drop()
    print("Dropped existing collections to prevent duplicates.")

    # Data generation sets
    cities = ["Udupi", "Manipal", "Mangalore", "Surathkal", "Kundapura"]
    first_names = ["Rahul", "Priya", "Arjun", "Sneha", "Karan", "Anjali", "Vikram", "Rohan", "Megha", "Neha", "Aditya", "Siddharth", "Aisha", "Kiran", "Nikhil", "Pooja", "Raj", "Riya", "Varun", "Kavya"]
    last_names = ["Shetty", "Rao", "Prabhu", "Naik", "Kamat", "Shenoy", "Bhat", "Pai", "Hegde", "Mallya", "Poojary", "Gowda"]
    
    # 1. Generate 50 Customers
    customers = []
    for i in range(1, 51):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        phone = f"9{random.randint(10000000, 99999999)}"
        customers.append({
            "_id": f"C{i:03d}",
            "name": name,
            "phone": phone,
            "city": random.choice(cities)
        })
    db.customers.insert_many(customers)
    print(f"Inserted {len(customers)} customers.")

    # 2. Generate 10 Restaurants
    restaurant_names = ["Food Palace", "Spice Hub", "Udupi Kitchen", "Manipal Cafe", "Tandoor Express", "Coastline Diner", "Biryani Central", "Dosa Corner", "Curry Leaves", "Sagar Ratna"]
    cuisines = ["Indian", "Chinese", "South Indian", "North Indian", "Continental", "Mughlai", "Fast Food"]
    restaurants = []
    for i in range(1, 11):
        restaurants.append({
            "_id": f"R{i:03d}",
            "name": restaurant_names[i-1],
            "location": random.choice(cities),
            "cuisine": random.choice(cuisines),
            "rating": round(random.uniform(3.5, 5.0), 1)
        })
    db.restaurants.insert_many(restaurants)
    print(f"Inserted {len(restaurants)} restaurants.")

    # 3. Generate 50 Food Items
    food_names = [
        "Chicken Biryani", "Mutton Biryani", "Paneer Butter Masala", "Veg Fried Rice", "Masala Dosa",
        "Idli Sambar", "Butter Chicken", "Dal Makhani", "Tandoori Roti", "Garlic Naan",
        "Gobi Manchurian", "Chicken Tikka", "Mushroom Chilli", "Veg Kadai", "Fish Curry",
        "Prawn Fry", "Egg Curry", "Aloo Paratha", "Chole Bhature", "Pav Bhaji",
        "Medu Vada", "Upma", "Neer Dosa", "Chicken Kebab", "Mutton Rogan Josh",
        "Palak Paneer", "Malai Kofta", "Jeera Rice", "Dal Tadka", "Chicken Noodles",
        "Veg Hakka Noodles", "Spring Roll", "Sweet Corn Soup", "Tomato Soup", "Chicken Manchow",
        "Fish Tikka", "Tandoori Chicken", "Chicken 65", "Veg Kolhapuri", "Mushroom Masala",
        "Puri Bhaji", "Rava Dosa", "Onion Uthappam", "Ghee Roast Dosa", "Chicken Sukka",
        "Kori Rotti", "Prawn Ghee Roast", "Bangda Fry", "Gulab Jamun", "Rasgulla"
    ]
    categories = ["Main Course", "Starters", "Breakfast", "Breads", "Soups", "Desserts", "Seafood"]
    food_items = []
    for i in range(1, 51):
        rest = random.choice(restaurants)
        price = random.choice([40, 60, 80, 100, 120, 150, 180, 200, 250, 300, 350])
        food_items.append({
            "_id": f"F{i:03d}",
            "name": food_names[i-1],
            "category": random.choice(categories),
            "price": price,
            "restaurant_id": rest["_id"]
        })
    db.food_items.insert_many(food_items)
    print(f"Inserted {len(food_items)} food items.")

    # 4. Generate 200 Orders
    statuses = ["Delivered", "Preparing", "Out for Delivery", "Cancelled"]
    payment_methods = ["UPI", "Cash", "Card"]
    orders = []
    
    for i in range(1, 201):
        order_id = f"ORD{i:03d}"
        customer = random.choice(customers)
        restaurant = random.choice(restaurants)
        
        # Get food items from this restaurant
        rest_foods = [f for f in food_items if f["restaurant_id"] == restaurant["_id"]]
        if not rest_foods:
            rest_foods = [random.choice(food_items)] # Fallback
            
        # Embedded items (1 to 4 items per order)
        num_items = random.randint(1, 4)
        items = []
        total_amount = 0
        
        chosen_foods = random.sample(rest_foods, min(num_items, len(rest_foods)))
        
        for food in chosen_foods:
            quantity = random.randint(1, 3)
            price = food["price"]
            items.append({
                "food_id": food["_id"],
                "name": food["name"],
                "quantity": quantity,
                "price": price
            })
            total_amount += (price * quantity)
            
        # Realistic Dates: spread over the last 30 days
        days_ago = random.randint(0, 30)
        ordered_at = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        # Realistic statuses and delivery time
        # Bias towards Delivered for realistic analytics
        status = random.choices(statuses, weights=[70, 10, 15, 5], k=1)[0]
        delivery_time = random.randint(20, 75) if status == "Delivered" else None
        
        orders.append({
            "_id": order_id,
            "customer_id": customer["_id"],
            "restaurant_id": restaurant["_id"],
            "items": items,
            "total_amount": total_amount,
            "payment_method": random.choice(payment_methods),
            "order_status": status,
            "ordered_at": ordered_at,
            "delivery_time_minutes": delivery_time
        })
        
    db.orders.insert_many(orders)
    print(f"Inserted {len(orders)} orders.")

    # Re-create indexes
    db.orders.create_index("customer_id")
    db.orders.create_index("restaurant_id")
    db.orders.create_index("ordered_at")
    
    print("SUCCESS: Database populated with realistic sample data!")

if __name__ == "__main__":
    load_sample_data()
