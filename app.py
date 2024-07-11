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
connect.execute('CREATE TABLE IF NOT EXISTS PARTICIPANTS (first_name TEXT, last_name TEXT, team INTEGER, email TEXT, phone TEXT, hashed_pass INTEGER)') 


@app.route('/join', methods=['GET', 'POST'])
def join(): 
	if request.method == 'POST': 
		first_name = request.form['first_name']
		last_name = request.form['last_name'] 
		email = request.form['email'] 
		phone = request.form['phone']
		team = request.form['team']
		hashed_pass = hash(request.form['pass'])

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
				cursor.execute("INSERT INTO PARTICIPANTS (first_name,last_name,team,email,phone,hashed_pass) VALUES (?,?,?,?,?,?)", (first_name, last_name, team, email,phone,hashed_pass)) 
				users.commit()
				return render_template("confirmation.html")
			else:
				return redirect("/full")

	else: 
		team = request.args.get("team")
		print(team)
		return render_template('join.html', team= int(team)) 

@app.route('/full', methods=['GET']) 
def full():
	return render_template("full.html")

@app.route('/remove', methods=['GET', 'POST'])
def remove(): 
	if request.method == 'POST': 
		entry = request.form['entry'].split()
		hashed_pass = hash(request.form['pass'])

		with sqlite3.connect("database.db") as users: 
			cursor = users.cursor() 
			cursor.execute('SELECT * FROM PARTICIPANTS') 
			entries = cursor.fetchall()
			formatted_entries = [[str(person[2]), person[0], person[1]] for person in entries]
			index = formatted_entries.index(entry)
			print(index)
			print("Correct pass: " + str(entries[index][5]))
			print("Attempted pass: " + str(hashed_pass))
			if entries[index][5] == hashed_pass:
				cursor.execute(f"DELETE FROM PARTICIPANTS WHERE first_name='{entry[1]}' AND last_name = '{entry[2]}' AND hashed_pass = '{hashed_pass}';")
				return render_template("leaving.html")
			else:
				return render_template("incorrect_password.html")
	else: 
		entry = request.args.get("entry").split()
		print(entry)

		with sqlite3.connect("database.db") as users: 
			cursor = users.cursor() 
			cursor.execute('SELECT * FROM PARTICIPANTS') 
			entries = cursor.fetchall()
			formatted_entries = sorted([[str(person[2]), person[0], person[1]] for person in entries])
			print(formatted_entries)
			return render_template('remove.html', user_entry=entry, entries=formatted_entries) 

if __name__ == '__main__':
	app.run(debug=False) 
