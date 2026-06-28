import plotly.express as px
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from db import conn

df = pd.read_sql(
    "SELECT * FROM sales",
    conn
)

# Load Data
df = pd.read_sql(
    "SELECT * FROM sales",
    conn
)


# convert date column
df['order_date'] = pd.to_datetime(df['order_date'])

# ----------
# dashboard title
# ---------
st.title("Sales Analytics Dashboard")

# ---------
#Sidebar Filters
# ---------
st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options = df['region'].unique(),
    default = df['region'].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options = df['category'].unique(),
    default = df['category'].unique()
)

# Date Filter
st.sidebar.header("Date Filter")
start_date = st.sidebar.date_input(
    "Start Date",
    df['order_date'].min()

)
end_date = st.sidebar.date_input(
    "End Date",
    df['order_date'].max()
)


# Filtered Data
filtered_df = df[
    (df['region'].isin(selected_region)) &
    (df['category'].isin(selected_category)) &
    (df['order_date'] >= pd.to_datetime(start_date)) &
    (df['order_date'] <= pd.to_datetime(end_date))
]

# ----------
# KPI card in one line
# ----------
# Avg Order
avg_order = (
    filtered_df['sales'].sum()
    /
    len(filtered_df)
)
st.metric(
    "Average Order Value",
    f"${avg_order:,.2f}"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰Total Sales",
        f"${filtered_df['sales'].sum():,.2f}"
    )

with col2:
    st.metric(
        "📈Total Profit",
        f"${filtered_df['sales'].sum():,.2f}"
    )

with col3:
    st.metric(
        "🛒Total Orders",
        len(filtered_df)
    )
with col4:
    st.metric(
        "Avg Order",
        f"${avg_order:,.2f}"
    )
st.markdown("---")

# ----------
# Sales By Region Charts
# ----------
region_sales=(
    filtered_df
    .groupby('region')['sales']
    .sum()
    .reset_index()
)

fig1 = px.bar(
    region_sales,
    x = 'region',
    y = 'sales',
    title = 'Sales By Region',
    text_auto = '.2s'
)
st.plotly_chart(
    fig1,
    use_container_width = True
)
# Sales Distributed Pie Charts
fig4 = px.pie(
    filtered_df,
    names = 'category',
    values = 'sales',
    title = 'Sales Distributed By Category'
)
st.plotly_chart(
    fig4,
    use_container_width = True
)

# Profit BY Region
profit_region = (
    filtered_df
    .groupby('region')['profit']
    .sum()
    .reset_index()
)
fig5 = px.bar(
    profit_region,
    x = 'region',
    y = 'profit',
    title = 'Profit By Region',
    text_auto = '.2s'
)
st.plotly_chart(
    fig5,
    use_container_width = True
)

# ----------
# Profit By Category 
# ----------
category_profit= (
    filtered_df
    .groupby('category')['profit']
    .sum()
    .reset_index()
)
fig2 = px.bar(
    category_profit,
    x = 'category',
    y = 'profit',
    title = 'Profit By Category',
    text_auto = '.2s'
)
st.plotly_chart(
    fig2,
    use_container_width=True
)

# ----------
# Monthly Sales Trend
# ----------
monthly_sales = (
    filtered_df
    .groupby(
        filtered_df['order_date']
        .dt.to_period('M')
    )['sales']
    .sum()
    .reset_index()
)
monthly_sales['order_date'] = (
    monthly_sales['order_date']
    .astype(str)
)

fig3 = px.line(
    monthly_sales,
    x = 'order_date',
    y = 'sales',
    title = 'Monthly Sales Trend',
    markers = True
)
st.plotly_chart(
    fig3,
    use_container_width= True
)

# ----------
# Top 10 Products
# ----------
top_products = (
    filtered_df
    .groupby('product_name')['sales']
    .sum()
    .sort_values(ascending = False)
    .head(10)
    .reset_index()
)
fig4 = px.bar(
    top_products,
    x = 'product_name',
    y = 'sales',
    title = 'Top 10 Product By Sales'

)
st.plotly_chart(
    fig4,
    use_container_width = True
)




# ----------
# Data Table
# ----------
st.subheader("Sales Data")
st.dataframe(
    filtered_df,
    use_container_width = True
)
# ----------
# Download Button
# ----------

csv = filtered_df.to_csv(
    index = False
).encode('utf-8')
st.download_button(
    label = "Download Report",
    data = csv,
    file_name="sales_report.csv",
    mime = "text/csv"
)