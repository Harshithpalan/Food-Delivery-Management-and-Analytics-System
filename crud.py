from datetime import datetime

# ==========================================
# CUSTOMERS CRUD
# ==========================================

def create_customer(db, customer_id, name, phone, city):
    try:
        # Check if ID already exists
        if db.customers.find_one({"_id": customer_id}):
            return False, f"Customer with ID {customer_id} already exists."
        
        customer = {
            "_id": customer_id,
            "name": name,
            "phone": phone,
            "city": city
        }
        db.customers.insert_one(customer)
        return True, "Customer added successfully."
    except Exception as e:
        return False, f"Error adding customer: {str(e)}"

def get_all_customers(db):
    try:
        return list(db.customers.find())
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return []

def search_customers(db, search_term):
    try:
        # Search by ID, name or phone using regex
        query = {
            "$or": [
                {"_id": {"$regex": search_term, "$options": "i"}},
                {"name": {"$regex": search_term, "$options": "i"}},
                {"phone": {"$regex": search_term, "$options": "i"}}
            ]
        }
        return list(db.customers.find(query))
    except Exception as e:
        print(f"Error searching customers: {e}")
        return []

def update_customer(db, customer_id, update_data):
    try:
        result = db.customers.update_one(
            {"_id": customer_id},
            {"$set": update_data}
        )
        if result.modified_count > 0:
            return True, "Customer updated successfully."
        return False, "No changes made or customer not found."
    except Exception as e:
        return False, f"Error updating customer: {str(e)}"

def delete_customer(db, customer_id):
    try:
        result = db.customers.delete_one({"_id": customer_id})
        if result.deleted_count > 0:
            return True, "Customer deleted successfully."
        return False, "Customer not found."
    except Exception as e:
        return False, f"Error deleting customer: {str(e)}"

# ==========================================
# RESTAURANTS CRUD
# ==========================================

def create_restaurant(db, restaurant_id, name, location, cuisine, rating):
    try:
        if db.restaurants.find_one({"_id": restaurant_id}):
            return False, f"Restaurant with ID {restaurant_id} already exists."
        
        restaurant = {
            "_id": restaurant_id,
            "name": name,
            "location": location,
            "cuisine": cuisine,
            "rating": float(rating)
        }
        db.restaurants.insert_one(restaurant)
        return True, "Restaurant added successfully."
    except Exception as e:
        return False, f"Error adding restaurant: {str(e)}"

def get_all_restaurants(db):
    try:
        return list(db.restaurants.find())
    except Exception as e:
        print(f"Error fetching restaurants: {e}")
        return []

def search_restaurants(db, search_term):
    try:
        query = {
            "$or": [
                {"_id": {"$regex": search_term, "$options": "i"}},
                {"name": {"$regex": search_term, "$options": "i"}},
                {"location": {"$regex": search_term, "$options": "i"}}
            ]
        }
        return list(db.restaurants.find(query))
    except Exception as e:
        print(f"Error searching restaurants: {e}")
        return []

def update_restaurant(db, restaurant_id, update_data):
    try:
        result = db.restaurants.update_one(
            {"_id": restaurant_id},
            {"$set": update_data}
        )
        if result.modified_count > 0:
            return True, "Restaurant updated successfully."
        return False, "No changes made or restaurant not found."
    except Exception as e:
        return False, f"Error updating restaurant: {str(e)}"

def delete_restaurant(db, restaurant_id):
    try:
        result = db.restaurants.delete_one({"_id": restaurant_id})
        if result.deleted_count > 0:
            return True, "Restaurant deleted successfully."
        return False, "Restaurant not found."
    except Exception as e:
        return False, f"Error deleting restaurant: {str(e)}"

# ==========================================
# FOOD ITEMS CRUD
# ==========================================

def create_food_item(db, food_id, name, category, price, restaurant_id):
    try:
        if db.food_items.find_one({"_id": food_id}):
            return False, f"Food item with ID {food_id} already exists."
            
        # Verify restaurant exists
        if not db.restaurants.find_one({"_id": restaurant_id}):
            return False, f"Restaurant with ID {restaurant_id} does not exist."
        
        food = {
            "_id": food_id,
            "name": name,
            "category": category,
            "price": float(price),
            "restaurant_id": restaurant_id
        }
        db.food_items.insert_one(food)
        return True, "Food item added successfully."
    except Exception as e:
        return False, f"Error adding food item: {str(e)}"

def get_all_food_items(db):
    try:
        return list(db.food_items.find())
    except Exception as e:
        print(f"Error fetching food items: {e}")
        return []

def search_food_items(db, search_term):
    try:
        query = {
            "$or": [
                {"_id": {"$regex": search_term, "$options": "i"}},
                {"name": {"$regex": search_term, "$options": "i"}},
                {"category": {"$regex": search_term, "$options": "i"}}
            ]
        }
        return list(db.food_items.find(query))
    except Exception as e:
        print(f"Error searching food items: {e}")
        return []

def update_food_item(db, food_id, update_data):
    try:
        result = db.food_items.update_one(
            {"_id": food_id},
            {"$set": update_data}
        )
        if result.modified_count > 0:
            return True, "Food item updated successfully."
        return False, "No changes made or food item not found."
    except Exception as e:
        return False, f"Error updating food item: {str(e)}"

def delete_food_item(db, food_id):
    try:
        result = db.food_items.delete_one({"_id": food_id})
        if result.deleted_count > 0:
            return True, "Food item deleted successfully."
        return False, "Food item not found."
    except Exception as e:
        return False, f"Error deleting food item: {str(e)}"

# ==========================================
# ORDERS CRUD
# ==========================================

def create_order(db, order_id, customer_id, restaurant_id, items, total_amount, payment_method):
    try:
        if db.orders.find_one({"_id": order_id}):
            return False, f"Order with ID {order_id} already exists."
            
        # Verify customer and restaurant
        if not db.customers.find_one({"_id": customer_id}):
            return False, f"Customer with ID {customer_id} does not exist."
        if not db.restaurants.find_one({"_id": restaurant_id}):
            return False, f"Restaurant with ID {restaurant_id} does not exist."
            
        order = {
            "_id": order_id,
            "customer_id": customer_id,
            "restaurant_id": restaurant_id,
            "items": items, # Embedded documents array
            "total_amount": float(total_amount),
            "payment_method": payment_method,
            "order_status": "Preparing",
            "ordered_at": datetime.now(),
            "delivery_time_minutes": None
        }
        db.orders.insert_one(order)
        return True, "Order placed successfully."
    except Exception as e:
        return False, f"Error creating order: {str(e)}"

def get_all_orders(db):
    try:
        return list(db.orders.find().sort("ordered_at", -1))
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return []

def search_orders(db, search_term):
    try:
        query = {
            "$or": [
                {"_id": {"$regex": search_term, "$options": "i"}},
                {"customer_id": {"$regex": search_term, "$options": "i"}},
                {"restaurant_id": {"$regex": search_term, "$options": "i"}},
                {"order_status": {"$regex": search_term, "$options": "i"}}
            ]
        }
        return list(db.orders.find(query).sort("ordered_at", -1))
    except Exception as e:
        print(f"Error searching orders: {e}")
        return []

def update_order_status(db, order_id, new_status, delivery_time=None):
    try:
        valid_statuses = ["Preparing", "Out for Delivery", "Delivered", "Cancelled"]
        if new_status not in valid_statuses:
            return False, f"Invalid status. Must be one of {valid_statuses}."
            
        update_data = {"order_status": new_status}
        if new_status == "Delivered" and delivery_time:
            update_data["delivery_time_minutes"] = int(delivery_time)
            
        result = db.orders.update_one(
            {"_id": order_id},
            {"$set": update_data}
        )
        if result.modified_count > 0:
            return True, f"Order status updated to {new_status}."
        return False, "Order not found or status is already the same."
    except Exception as e:
        return False, f"Error updating order status: {str(e)}"

def cancel_order(db, order_id):
    try:
        order = db.orders.find_one({"_id": order_id})
        if not order:
            return False, "Order not found."
            
        if order.get("order_status") in ["Delivered", "Cancelled"]:
            return False, f"Cannot cancel an order that is already {order.get('order_status')}."
            
        result = db.orders.update_one(
            {"_id": order_id},
            {"$set": {"order_status": "Cancelled"}}
        )
        return True, "Order cancelled successfully."
    except Exception as e:
        return False, f"Error cancelling order: {str(e)}"
