from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib # used for hashing passwords

app = Flask(__name__) 

connect = sqlite3.connect('database.db') 
connect.execute('CREATE TABLE IF NOT EXISTS PARTICIPANTS (first_name TEXT, last_name TEXT, team INTEGER, email TEXT, phone TEXT, hashed_pass INTEGER, id INTEGER PRIMARY KEY, checked_in INTEGER);') 


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


@app.route('/join', methods=['GET', 'POST'])
def join(): 
	if request.method == 'POST': 
		first_name = request.form['first_name']
		last_name = request.form['last_name'] 
		email = request.form['email'] 
		phone = request.form['phone']
		team = request.form['team']
		hashed_pass = hashlib.sha256(request.form['pass'].encode()).hexdigest()

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
				cursor.execute("INSERT INTO PARTICIPANTS (first_name,last_name,team,email,phone,hashed_pass,checked_in) VALUES (?,?,?,?,?,?,?)", (first_name, last_name, team, email,phone,hashed_pass,0)) 
				users.commit()
				return render_template("register_confirmation.html")
			else:
				return redirect("/full")

	else:
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

		team = request.args.get("team")
		print(team)
		if team == None:
			team = 1
		return render_template('join.html', team=int(team), capacities=capacities) 

@app.route('/full', methods=['GET'])
def full():
	return render_template("full.html")

@app.route('/remove', methods=['GET', 'POST'])
def remove(): 
	if request.method == 'POST': 

		entry_id = request.form['entry']
		hashed_pass = hashlib.sha256(request.form['pass'].encode()).hexdigest()

		with sqlite3.connect("database.db") as users: 
			cursor = users.cursor() 
			cursor.execute(f'SELECT * FROM PARTICIPANTS WHERE id = {entry_id}') 
			target_entry = cursor.fetchall()

			if target_entry[0][7] == 1:
				return render_template("already_checked_in.html")
			elif target_entry[0][5] == hashed_pass:
				cursor.execute(f"DELETE FROM PARTICIPANTS WHERE id = '{entry_id}' AND hashed_pass = '{hashed_pass}';")
				return render_template("leaving.html")
			else:
				return render_template("incorrect_password.html")
	else: 
		entry_id = request.args.get("entry")
		print(entry_id)

		with sqlite3.connect("database.db") as users:
			cursor = users.cursor()
			cursor.execute('SELECT * FROM PARTICIPANTS')
			entries = cursor.fetchall()
			cursor.execute(f'SELECT * FROM PARTICIPANTS WHERE id = "{entry_id}"')
			try:
				entry=cursor.fetchall()[0]
			except Exception as e:
				return render_template('error.html', error_msg=e)
			return render_template('remove.html', user_entry=entry, entries=entries)
		
@app.route('/checkin', methods=['GET', 'POST'])
def checkin(): 
	if request.method == 'POST': 

		entry_id = request.form['entry']
		hashed_pass = hashlib.sha256(request.form['pass'].encode()).hexdigest()

		with sqlite3.connect("database.db") as users: 
			cursor = users.cursor() 
			cursor.execute(f'SELECT * FROM PARTICIPANTS WHERE id = {entry_id}') 
			target_entry = cursor.fetchall()


			if target_entry[0][5] == hashed_pass:
				cursor.execute(f"UPDATE PARTICIPANTS SET checked_in = 1 WHERE id = '{entry_id}' AND hashed_pass = '{hashed_pass}';")
				return render_template("check_in_confirmation.html")
			else:
				return render_template("incorrect_password.html")
	else: 
		entry_id = request.args.get("entry")
		print(entry_id)

		with sqlite3.connect("database.db") as users:
			cursor = users.cursor()
			cursor.execute('SELECT * FROM PARTICIPANTS')
			entries = cursor.fetchall()
			cursor.execute(f'SELECT * FROM PARTICIPANTS WHERE id = "{entry_id}"')
			try:
				entry=cursor.fetchall()[0]
			except Exception as e:
				return render_template('error.html', error_msg=e)
			return render_template('checkin.html', user_entry=entry, entries=entries)
		
@app.route('/password', methods=['GET'])
def password():
	team = request.args.get("team")
	return render_template('password_handling.html', team=int(team))

if __name__ == '__main__':
	app.run(debug=False) 
