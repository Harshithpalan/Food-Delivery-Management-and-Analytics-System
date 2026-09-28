import streamlit as st
import pandas as pd
import crud

def manage_food_items(db):
    st.header("Food Items Management")
    
    tabs = st.tabs(["Add Food Item", "View & Search", "Update", "Delete"])
    
    # Pre-fetch restaurants for dropdowns
    restaurants = crud.get_all_restaurants(db)
    rest_options = {r["_id"]: f"{r['name']} ({r['_id']})" for r in restaurants}
    
    with tabs[0]:
        st.subheader("Add New Food Item")
        if not restaurants:
            st.error("You must add a restaurant before adding food items.")
        else:
            with st.form("add_food_form"):
                f_id = st.text_input("Food ID")
                name = st.text_input("Food Name")
                category = st.text_input("Category")
                price = st.number_input("Price (₹)", min_value=1.0, value=100.0)
                r_id = st.selectbox("Assign to Restaurant", options=list(rest_options.keys()), format_func=lambda x: rest_options[x])
                
                submit = st.form_submit_button("Add Food Item")
                
                if submit:
                    if f_id and name and category:
                        success, msg = crud.create_food_item(db, f_id, name, category, price, r_id)
                        if success: st.success(msg)
                        else: st.error(msg)
                    else:
                        st.warning("Please fill all fields.")
                    
    with tabs[1]:
        st.subheader("View Food Items")
        search = st.text_input("Search Food by ID, Name or Category")
        if search:
            data = crud.search_food_items(db, search)
        else:
            data = crud.get_all_food_items(db)
            
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.write("No food items found.")
            
    with tabs[2]:
        st.subheader("Update Food Details")
        f_id_upd = st.text_input("Enter Food ID to update")
        upd_name = st.text_input("New Name (leave blank to skip)")
        upd_price = st.number_input("New Price (set to 0 to skip)", min_value=0.0, value=0.0)
        
        if st.button("Update Food Item"):
            if f_id_upd:
                updates = {}
                if upd_name: updates["name"] = upd_name
                if upd_price > 0: updates["price"] = upd_price
                
                if updates:
                    success, msg = crud.update_food_item(db, f_id_upd, updates)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("No fields provided to update.")
            else:
                st.warning("Food ID required.")
                
    with tabs[3]:
        st.subheader("Delete Food Item")
        f_id_del = st.text_input("Enter Food ID to delete")
        if st.button("Delete Food Item"):
            if f_id_del:
                success, msg = crud.delete_food_item(db, f_id_del)
                if success: st.success(msg)
                else: st.error(msg)
            else:
                st.warning("Food ID required.")
