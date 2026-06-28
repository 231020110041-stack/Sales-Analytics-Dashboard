import pandas as pd
from db import conn

query = "SELECT * FROM sales"
df = pd.read_sql(query, conn)

print(df.head())
print(df.info())

print("Total Sales:", df['sales'].sum())
print("Total Profit:", df['profit'].sum())
print("Total Order:" , len(df))

print(df.groupby('region')['sales'].sum())
print(df.groupby('category')['category'].sum())
