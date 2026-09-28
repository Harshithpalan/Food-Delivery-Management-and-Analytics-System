import streamlit as st
import pandas as pd
import crud

def manage_orders(db):
    st.header("Order Management")
    
    tabs = st.tabs(["Create Order", "View Orders", "Update/Cancel Order"])
    
    with tabs[0]:
        st.subheader("Place a New Order")
        customers = crud.get_all_customers(db)
        restaurants = crud.get_all_restaurants(db)
        
        if not customers or not restaurants:
            st.error("You need at least 1 customer and 1 restaurant in the database.")
            return
            
        c_opts = {c["_id"]: f"{c['name']} ({c['_id']})" for c in customers}
        r_opts = {r["_id"]: f"{r['name']} ({r['_id']})" for r in restaurants}
        
        col1, col2 = st.columns(2)
        with col1:
            sel_c_id = st.selectbox("Select Customer", options=list(c_opts.keys()), format_func=lambda x: c_opts[x])
        with col2:
            sel_r_id = st.selectbox("Select Restaurant", options=list(r_opts.keys()), format_func=lambda x: r_opts[x])
            
        # Fetch food for selected restaurant
        all_food = crud.get_all_food_items(db)
        rest_food = [f for f in all_food if f["restaurant_id"] == sel_r_id]
        
        st.divider()
        if not rest_food:
            st.warning("This restaurant has no food items on the menu.")
        else:
            st.write("#### Menu & Quantities")
            order_items = []
            total_amount = 0
            
            # Create a nice layout for food selection
            for f in rest_food:
                f_col1, f_col2 = st.columns([3, 1])
                f_col1.write(f"**{f['name']}** - ₹{f['price']}")
                qty = f_col2.number_input(f"Qty##{f['_id']}", min_value=0, max_value=20, value=0)
                
                if qty > 0:
                    order_items.append({
                        "food_id": f["_id"],
                        "name": f["name"],
                        "quantity": qty,
                        "price": f["price"]
                    })
                    total_amount += (f["price"] * qty)
                    
            st.divider()
            st.write(f"### Total Amount: ₹{total_amount}")
            
            with st.form("create_order_form"):
                order_id = st.text_input("Order ID")
                payment = st.selectbox("Payment Method", ["UPI", "Card", "Cash"])
                submit = st.form_submit_button("Place Order")
                
                if submit:
                    if not order_id:
                        st.error("Order ID is required.")
                    elif len(order_items) == 0:
                        st.error("You must select at least one item to place an order.")
                    else:
                        success, msg = crud.create_order(db, order_id, sel_c_id, sel_r_id, order_items, total_amount, payment)
                        if success: st.success(msg)
                        else: st.error(msg)
                        
    with tabs[1]:
        st.subheader("View Order History")
        search = st.text_input("Search Orders by ID, Customer ID, or Status")
        if search:
            data = crud.search_orders(db, search)
        else:
            data = crud.get_all_orders(db)
            
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.write("No orders found.")
            
    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Update Order Status")
            upd_id = st.text_input("Order ID to update status")
            new_status = st.selectbox("New Status", ["Preparing", "Out for Delivery", "Delivered"])
            del_time = None
            if new_status == "Delivered":
                del_time = st.number_input("Delivery Time (minutes)", min_value=1, value=30)
            
            if st.button("Update Status"):
                if upd_id:
                    success, msg = crud.update_order_status(db, upd_id, new_status, del_time)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Order ID required.")
                    
        with col2:
            st.subheader("Cancel Order")
            canc_id = st.text_input("Order ID to cancel")
            if st.button("Cancel Order", type="primary"):
                if canc_id:
                    success, msg = crud.cancel_order(db, canc_id)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Order ID required.")
