# analytics_db.py
# Contains all MongoDB Aggregation Pipelines for Data Analytics

def get_total_revenue(db):
    pipeline = [
        {"$group": {"_id": None, "total_revenue": {"$sum": "$total_amount"}}}
    ]
    result = list(db.orders.aggregate(pipeline))
    return result[0]["total_revenue"] if result else 0

def get_total_orders(db):
    # We can just use count_documents, but to use aggregation:
    pipeline = [
        {"$count": "total_orders"}
    ]
    result = list(db.orders.aggregate(pipeline))
    return result[0]["total_orders"] if result else 0

def get_top_restaurants(db, limit=5):
    pipeline = [
        {"$group": {
            "_id": "$restaurant_id",
            "revenue": {"$sum": "$total_amount"},
            "orders": {"$sum": 1}
        }},
        {"$lookup": {
            "from": "restaurants",
            "localField": "_id",
            "foreignField": "_id",
            "as": "restaurant_details"
        }},
        {"$unwind": "$restaurant_details"},
        {"$project": {
            "restaurant_name": "$restaurant_details.name",
            "revenue": 1,
            "orders": 1
        }},
        {"$sort": {"revenue": -1}},
        {"$limit": limit}
    ]
    return list(db.orders.aggregate(pipeline))

def get_popular_food_items(db, limit=10):
    pipeline = [
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.food_id",
            "food_name": {"$first": "$items.name"},
            "total_quantity": {"$sum": "$items.quantity"},
            "revenue_generated": {"$sum": {"$multiply": ["$items.price", "$items.quantity"]}}
        }},
        {"$sort": {"total_quantity": -1}},
        {"$limit": limit}
    ]
    return list(db.orders.aggregate(pipeline))

def get_orders_by_status(db):
    pipeline = [
        {"$group": {
            "_id": "$order_status",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    return list(db.orders.aggregate(pipeline))

def get_average_delivery_time(db):
    pipeline = [
        {"$match": {"order_status": "Delivered", "delivery_time_minutes": {"$ne": None}}},
        {"$group": {
            "_id": None,
            "avg_time": {"$avg": "$delivery_time_minutes"}
        }}
    ]
    result = list(db.orders.aggregate(pipeline))
    return round(result[0]["avg_time"], 1) if result else 0

def get_customer_spending(db, limit=10):
    pipeline = [
        {"$group": {
            "_id": "$customer_id",
            "total_spent": {"$sum": "$total_amount"},
            "total_orders": {"$sum": 1}
        }},
        {"$lookup": {
            "from": "customers",
            "localField": "_id",
            "foreignField": "_id",
            "as": "customer_details"
        }},
        {"$unwind": "$customer_details"},
        {"$project": {
            "customer_name": "$customer_details.name",
            "total_spent": 1,
            "total_orders": 1
        }},
        {"$sort": {"total_spent": -1}},
        {"$limit": limit}
    ]
    return list(db.orders.aggregate(pipeline))

def get_revenue_by_date(db):
    pipeline = [
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$ordered_at"}},
            "daily_revenue": {"$sum": "$total_amount"},
            "orders_count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}} # Sort by date ascending
    ]
    return list(db.orders.aggregate(pipeline))
