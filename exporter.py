import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect('database.db')

# Write the name of your table
table_name = 'PARTICIPANTS'

# Read the table into a pandas DataFrame
df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

# Export the DataFrame to a CSV file
df.to_csv('output.csv', index=False)

# Close the database connection
conn.close()

print(f"Table '{table_name}' has been exported to 'output.csv'")