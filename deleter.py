import sqlite3 

id = 1

connect = sqlite3.connect('database.db') 
cursor = connect.cursor()
cursor.execute(f"DELETE FROM PARTICIPANTS WHERE id={id};")
connect.commit()

print("Done.")

connect.close()