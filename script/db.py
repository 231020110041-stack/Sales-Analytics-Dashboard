import mysql.connector
conn = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "Suraj@003",
    database = "sales_dashboard"
)

cursor = conn.cursor()