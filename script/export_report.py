import pandas as pd
from db import conn

query = "SELECT * FROM sales"
df = pd.read_sql(query, conn)

df.to_excel('sales_report.xlsx', index=False)

print("Report Exported Successfully!")