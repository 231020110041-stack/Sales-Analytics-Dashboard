import matplotlib.pyplot as plt
import pandas as pd
from db import conn
query = "SELECT* FROM sales"
df = pd.read_sql(query,conn)

# sales by region
region_sales = df.groupby('region')['sales'].sum()

region_sales.plot(kind='bar')
plt.title('Sales By Region')
plt.ylabel('Sales')
plt.show()



# Profit By Category

category_profit = df.groupby('category')['profit'].sum()

category_profit.plot(kind='bar')
plt.title('Profit By Category')
plt.ylabel('Profit')
plt.show()


# Monthly Sales Trend
df['order_date'] = pd.to_datetime(df['order_date'])

monthly_sales = (
    df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum()
)

monthly_sales.index = monthly_sales.index.astype(str)
monthly_sales.plot(kind='bar')
plt.title('Monthly Sales Trend')
plt.ylabel('Sales')
plt.xticks(rotation = 45)
plt.show()

# Top 10 Products By Sales

top_products = (
    df.groupby('product_name')['sales']
    .sum()
    .sort_values(ascending = False)
    .head(10)
)
top_products.plot(kind='bar')
plt.title("Top 10 Products")
plt.ylabel('Sales')
plt.xticks(rotation = 90)
plt.show()
