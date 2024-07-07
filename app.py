from flask import Flask, render_template, request 
import sqlite3 

app = Flask(__name__) 


@app.route('/') 
@app.route('/home') 
def index(): 
	connect = sqlite3.connect('database.db') 
	cursor = connect.cursor() 
	cursor.execute('SELECT * FROM PARTICIPANTS') 

	data = cursor.fetchall() 
	return render_template("home.html", data=data)


connect = sqlite3.connect('database.db') 
connect.execute('CREATE TABLE IF NOT EXISTS PARTICIPANTS (first_name TEXT, last_name TEXT, email TEXT, phone TEXT)') 


@app.route('/join', methods=['GET', 'POST']) 
def join(): 
	if request.method == 'POST': 
		first_name = request.form['first_name']
		last_name = request.form['last_name'] 
		email = request.form['email'] 
		phone = request.form['phone'] 

		with sqlite3.connect("database.db") as users: 
			cursor = users.cursor() 
			cursor.execute("INSERT INTO PARTICIPANTS (first_name,last_name,email,phone) VALUES (?,?,?,?)", (first_name, last_name, email, phone)) 
			users.commit() 
		return render_template("home.html") 
	else: 
		return render_template('join.html') 


if __name__ == '__main__': 
	app.run(debug=False) 
