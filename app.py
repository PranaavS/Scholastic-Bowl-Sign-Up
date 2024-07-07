from flask import Flask, render_template, request, redirect
import sqlite3 

app = Flask(__name__) 


@app.route('/') 
@app.route('/home') 
def index(): 
	connect = sqlite3.connect('database.db') 
	cursor = connect.cursor() 
	cursor.execute('SELECT * FROM PARTICIPANTS') 

	data = cursor.fetchall()
	capacities_dict = {
		"Team 1": 0,
		"Team 2": 0,
		"Team 3": 0,
		"Team 4": 0,
		"Team 5": 0,
		"Team 6": 0,
		"Team 7": 0,
		"Team 8": 0,
	}
	for participant in data:
		capacities_dict[f"Team {participant[2]}"] += 1
	
	capacities = [value for key, value in capacities_dict.items()]
	return render_template("new_home.html", data=data, capacities=capacities)


connect = sqlite3.connect('database.db') 
connect.execute('CREATE TABLE IF NOT EXISTS PARTICIPANTS (first_name TEXT, last_name TEXT, team INTEGER, email TEXT, phone TEXT)') 


@app.route('/join', methods=['GET', 'POST']) 
def join(): 
	if request.method == 'POST': 
		first_name = request.form['first_name']
		last_name = request.form['last_name'] 
		email = request.form['email'] 
		phone = request.form['phone']
		team = request.form['team']

		with sqlite3.connect("database.db") as users: 
			cursor = users.cursor() 
			cursor.execute('SELECT * FROM PARTICIPANTS') 
			data = cursor.fetchall()
			print(data)
			capacities_dict = {
				"Team 1": 0,
				"Team 2": 0,
				"Team 3": 0,
				"Team 4": 0,
				"Team 5": 0,
				"Team 6": 0,
				"Team 7": 0,
				"Team 8": 0,
			}
			for participant in data:
				capacities_dict[f"Team {participant[2]}"] += 1
			print(capacities_dict)
			print(capacities_dict[f"Team {team}"] < 5)
			
			if capacities_dict[f"Team {team}"] < 5:
				cursor.execute("INSERT INTO PARTICIPANTS (first_name,last_name,team,email,phone) VALUES (?,?,?,?,?)", (first_name, last_name, team, email,phone)) 
				users.commit()
			else:
				return redirect("/full")
		return redirect("/") 
	else: 
		return render_template('join.html') 

@app.route('/full', methods=['GET']) 
def full():
	return render_template("full.html")

if __name__ == '__main__': 
	app.run(debug=False) 
