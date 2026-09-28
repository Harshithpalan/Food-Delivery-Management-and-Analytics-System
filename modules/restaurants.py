import streamlit as st
import pandas as pd
import crud

def manage_restaurants(db):
    st.header("Restaurant Management")
    
    tabs = st.tabs(["Add Restaurant", "View & Search", "Update", "Delete"])
    
    with tabs[0]:
        st.subheader("Add New Restaurant")
        with st.form("add_rest_form"):
            r_id = st.text_input("Restaurant ID")
            name = st.text_input("Restaurant Name")
            location = st.text_input("Location / City")
            cuisine = st.text_input("Cuisine Type")
            rating = st.number_input("Initial Rating", min_value=1.0, max_value=5.0, value=5.0)
            submit = st.form_submit_button("Add Restaurant")
            
            if submit:
                if r_id and name and location and cuisine:
                    success, msg = crud.create_restaurant(db, r_id, name, location, cuisine, rating)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Please fill all text fields.")
                    
    with tabs[1]:
        st.subheader("View Restaurants")
        search = st.text_input("Search by ID, Name or Location")
        if search:
            data = crud.search_restaurants(db, search)
        else:
            data = crud.get_all_restaurants(db)
            
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.write("No restaurants found.")
            
    with tabs[2]:
        st.subheader("Update Restaurant Details")
        r_id_upd = st.text_input("Enter Restaurant ID to update")
        upd_name = st.text_input("New Name (leave blank to keep current)")
        upd_loc = st.text_input("New Location (leave blank to keep current)")
        upd_cuisine = st.text_input("New Cuisine (leave blank to keep current)")
        
        if st.button("Update Restaurant"):
            if r_id_upd:
                updates = {}
                if upd_name: updates["name"] = upd_name
                if upd_loc: updates["location"] = upd_loc
                if upd_cuisine: updates["cuisine"] = upd_cuisine
                
                if updates:
                    success, msg = crud.update_restaurant(db, r_id_upd, updates)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("No fields provided to update.")
            else:
                st.warning("Restaurant ID required.")
                
    with tabs[3]:
        st.subheader("Delete Restaurant")
        r_id_del = st.text_input("Enter Restaurant ID to delete")
        if st.button("Delete Restaurant"):
            if r_id_del:
                success, msg = crud.delete_restaurant(db, r_id_del)
                if success: st.success(msg)
                else: st.error(msg)
            else:
                st.warning("Restaurant ID required.")
