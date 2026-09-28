import streamlit as st
from database import get_database_connection, initialize_indexes, get_all_indexes
from modules import customers, restaurants, food_items, orders, analytics
import analytics_db
from foodos_theme import inject_theme, page_header, kpi_row, section

def main():
    st.set_page_config(page_title="Food Delivery OS", page_icon="🍔", layout="wide")
    inject_theme()
    
    db, client = get_database_connection()
    if db is None:
        st.error("Database connection failed. Is MongoDB running?")
        return

    st.sidebar.title("🍔 FoodOS")
    st.sidebar.markdown("---")
    menu = ["Dashboard", "Customers", "Restaurants", "Food Items", "Orders", "Analytics"]
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Dashboard":
        page_header("System", "Overview", "Real-time statistics and database control center.")
        
        # Calculate dynamic values from MongoDB
        total_cust = db.customers.count_documents({})
        total_rest = db.restaurants.count_documents({})
        total_food = db.food_items.count_documents({})
        total_ord = analytics_db.get_total_orders(db)
        total_rev = analytics_db.get_total_revenue(db)
        avg_time = float(analytics_db.get_average_delivery_time(db))
        
        kpi_row([
            {"icon": "👥", "label": "Total Customers",  "value": total_cust},
            {"icon": "🏪", "label": "Total Restaurants", "value": total_rest,  "accent": "#FF5A45"},
            {"icon": "🍕", "label": "Total Food Items",  "value": total_food,  "accent": "#7BD389"},
            {"icon": "📦", "label": "Total Orders",      "value": total_ord},
            {"icon": "💰", "label": "Total Revenue",     "value": total_rev, "prefix": "₹", "accent": "#FF5A45"},
            {"icon": "⏱️", "label": "Avg Delivery Time", "value": avg_time, "suffix": " mins", "accent": "#7BD389"},
        ])
        
        st.divider()
        section("🔧", "System Diagnostics")
        initialize_indexes(db)
        with st.expander("View Active MongoDB Indexes"):
            st.json(get_all_indexes(db))

    elif choice == "Customers":
        customers.manage_customers(db)
    elif choice == "Restaurants":
        restaurants.manage_restaurants(db)
    elif choice == "Food Items":
        food_items.manage_food_items(db)
    elif choice == "Orders":
        orders.manage_orders(db)
    elif choice == "Analytics":
        analytics.show_analytics(db)

if __name__ == "__main__":
    main()
