import sqlite3 

first_name_to_delete = "Pranaav"
last_name_to_delete = "Sureshkumar"

connect = sqlite3.connect('database.db') 
cursor = connect.cursor()
data = cursor.execute(f"DELETE FROM PARTICIPANTS WHERE first_name='{first_name_to_delete}' AND last_name = '{last_name_to_delete}';")
connect.commit()

print(data.fetchall())

connect.close()