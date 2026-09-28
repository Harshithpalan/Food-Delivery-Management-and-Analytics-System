import streamlit as st
import pandas as pd
import plotly.express as px
import analytics_db
from foodos_theme import page_header, kpi_row

def show_analytics(db):
    page_header("Business", "Analytics", "In-depth operational insights generated directly from MongoDB aggregation pipelines.")
    st.divider()
    
    # Calculate values
    total_rev = analytics_db.get_total_revenue(db)
    total_ord = analytics_db.get_total_orders(db)
    avg_time = float(analytics_db.get_average_delivery_time(db))
    
    # High Level KPIs using theme
    kpi_row([
        {"icon": "💰", "label": "Gross Revenue", "value": total_rev, "prefix": "₹", "accent": "#FF5A45"},
        {"icon": "📦", "label": "Completed Orders", "value": total_ord},
        {"icon": "⏱️", "label": "Average Delivery", "value": avg_time, "suffix": " mins", "accent": "#7BD389"},
    ])

    st.write("") # Spacer

    # Modern color sequence for charts matching the dark theme
    custom_colors = ['#FFB627', '#7BD389', '#FF5A45', '#9FB0B3', '#3b82f6', '#ec4899', '#14b8a6']
    # We will use plotly_dark template since the theme is dark
    chart_template = "plotly_dark"

    col1, col2 = st.columns(2)
    
    # Top Restaurants
    with col1:
        top_rest = analytics_db.get_top_restaurants(db, 5)
        if top_rest:
            df_rest = pd.DataFrame(top_rest)
            fig = px.bar(df_rest, x="restaurant_name", y="revenue", 
                         title="Top 5 Restaurants by Revenue", 
                         color="restaurant_name",
                         color_discrete_sequence=custom_colors,
                         template=chart_template,
                         labels={"restaurant_name": "Restaurant", "revenue": "Revenue (₹)"})
            fig.update_layout(showlegend=False, margin=dict(t=40, b=0, l=0, r=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    # Orders by Status
    with col2:
        status_data = analytics_db.get_orders_by_status(db)
        if status_data:
            df_status = pd.DataFrame(status_data)
            fig = px.pie(df_status, names="_id", values="count", 
                         title="Order Status Distribution",
                         hole=0.5,
                         color_discrete_sequence=custom_colors,
                         template=chart_template)
            fig.update_layout(margin=dict(t=40, b=0, l=0, r=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    st.write("")
    col3, col4 = st.columns(2)
    
    # Most Popular Food Items
    with col3:
        top_food = analytics_db.get_popular_food_items(db, 8)
        if top_food:
            df_food = pd.DataFrame(top_food)
            df_food = df_food.sort_values(by="total_quantity", ascending=True)
            fig = px.bar(df_food, x="total_quantity", y="food_name", orientation='h', 
                         title="Most Ordered Food Items",
                         color="total_quantity",
                         color_continuous_scale="solar",
                         template=chart_template,
                         labels={"food_name": "Item", "total_quantity": "Quantity Sold"})
            fig.update_layout(margin=dict(t=40, b=0, l=0, r=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    # Top Customers
    with col4:
        cust_spending = analytics_db.get_customer_spending(db, 7)
        if cust_spending:
            df_cust = pd.DataFrame(cust_spending)
            fig = px.bar(df_cust, x="customer_name", y="total_spent", 
                         title="Top Customer Spending",
                         color_discrete_sequence=['#FFB627'],
                         template=chart_template,
                         labels={"customer_name": "Customer", "total_spent": "Spent (₹)"})
            fig.update_layout(margin=dict(t=40, b=0, l=0, r=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    st.write("")
    
    # Revenue by Date
    rev_date = analytics_db.get_revenue_by_date(db)
    if rev_date:
        df_date = pd.DataFrame(rev_date)
        fig = px.line(df_date, x="_id", y="daily_revenue", 
                      title="Revenue Time Series", markers=True,
                      color_discrete_sequence=['#7BD389'],
                      template=chart_template,
                      labels={"_id": "Date", "daily_revenue": "Revenue (₹)"})
        
        # Fill area under curve
        fig.update_traces(fill='tozeroy', fillcolor='rgba(123, 211, 137, 0.2)')
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
