import pandas as pd
from db import conn
query = "SELECT * FROM sales"
df = pd.read_sql(query, conn)

summary = df.groupby('region').agg({
    'sales': 'sum',
    'profit': 'sum'

})

summary.to_excel('sales_report.xlsx')
print("Report Exported Successfully!")