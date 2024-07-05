from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def get_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, team TEXT)''')
    conn.commit()
    conn.close()

# Define a route and render a template
@app.route('/')
def index():
    get_db()
    print(c.fetchall())
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)