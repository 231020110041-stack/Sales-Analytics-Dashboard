import pandas as pd
from db import conn , cursor

df = pd.read_csv("/Users/surajtomar003/Downloads/sales_data.csv", encoding="latin1")

df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    format='%m/%d/%Y'
).dt.strftime('%Y-%m-%d')

for _, row in df.iterrows():
    sql = """
    INSERT INTO sales
    (order_id , order_date, region , category,
    product_name, sales, quantity ,profit)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (

        row['Order ID'],
        row['Order Date'],
        row['Region'],
        row['Category'],
        row['Product Name'],
        row['Sales'],
        row['Quantity'],
        row['Profit']

 )
    cursor.execute(sql, values)
conn.commit()
print("Data Imported Successfully")
