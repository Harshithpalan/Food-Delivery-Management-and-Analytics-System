import streamlit as st
import pandas as pd
import crud

def manage_customers(db):
    st.header("Customer Management")
    
    tabs = st.tabs(["Add Customer", "View & Search", "Update", "Delete"])
    
    with tabs[0]:
        st.subheader("Add New Customer")
        with st.form("add_cust_form"):
            c_id = st.text_input("Customer ID")
            name = st.text_input("Name")
            phone = st.text_input("Phone Number")
            city = st.text_input("City")
            submit = st.form_submit_button("Add Customer")
            
            if submit:
                if c_id and name and phone and city:
                    success, msg = crud.create_customer(db, c_id, name, phone, city)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Please fill all fields.")
                    
    with tabs[1]:
        st.subheader("View Customers")
        search = st.text_input("Search by ID, Name or Phone")
        if search:
            data = crud.search_customers(db, search)
        else:
            data = crud.get_all_customers(db)
            
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.write("No customers found.")
            
    with tabs[2]:
        st.subheader("Update Customer Details")
        c_id_upd = st.text_input("Enter Customer ID to update")
        upd_name = st.text_input("New Name (leave blank to keep current)")
        upd_phone = st.text_input("New Phone (leave blank to keep current)")
        upd_city = st.text_input("New City (leave blank to keep current)")
        
        if st.button("Update Customer"):
            if c_id_upd:
                updates = {}
                if upd_name: updates["name"] = upd_name
                if upd_phone: updates["phone"] = upd_phone
                if upd_city: updates["city"] = upd_city
                
                if updates:
                    success, msg = crud.update_customer(db, c_id_upd, updates)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("No fields provided to update.")
            else:
                st.warning("Customer ID required.")
                
    with tabs[3]:
        st.subheader("Delete Customer")
        c_id_del = st.text_input("Enter Customer ID to delete")
        if st.button("Delete Customer"):
            if c_id_del:
                success, msg = crud.delete_customer(db, c_id_del)
                if success: st.success(msg)
                else: st.error(msg)
            else:
                st.warning("Customer ID required.")
