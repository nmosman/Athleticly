from flask import Flask, render_template, request, session
from flaskext.mysql import MySQL
import os 
import sys

mysql = MySQL()
app = Flask(__name__); 




athlete_data = ""
coach_data = ""
ath_ID = ""
coach_ID = ""
admin_ID = ""

app.config['MYSQL_DATABASE_USER'] = 'root' 
app.config['MYSQL_DATABASE_PASSWORD'] = '7F28B138E09747CBA035CDCA81E0012470F7F413D58242ABAAD4215FEE805524'
app.config['MYSQL_DATABASE_DB'] = 'Athleticly'
app.config['MYSQL_DATABASE_HOST']  = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
	if not session.get('ath_in'):
		 return render_template('index.html')
	else:
		return "Hello Boss!"
   
		

@app.route("/admin")
def blah():
	if(session['admin']):
		return render_template('athlete_admin.html')
	else:
		return render_template('index.html')




@app.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
	global admin_ID
	adminId = request.form['AdminId']
	password = request.form['Password']

	admin_ID = adminId
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Admins where AdminId ='" + adminId + "' and Password = '" + password +"'")
	data = cursor.fetchone()
	print("ayyy", file = sys.stderr)
	print(data, file = sys.stderr)
	if data is None:
		return main()
	else:
		session['admin'] = True
		return admin(data)


@app.route('/admin')
def admin(data):
	return render_template('athlete_admin.html', data = data)

@app.route('/athlete_admin')
def athlete_admin():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Athletes")
	data = cursor.fetchall()

	return render_template('athlete_admin.html', data = data)

@app.route('/coach_admin')
def coach_admin():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Coaches")
	data = cursor.fetchall()
	return render_template('coach_admin.html', data = data)


@app.route('/adddelete')
def adddelete():
	if(session['coach'] or session['admin']):
		return render_template('adddelete.html')
	else:
		return main()

@app.route('/coachlist')
def coachlist():
	if(session['coach']):
		return render_template('coachlist.html')
	else:
		return main()


@app.route('/editathlete')
def editathlete():
	if(session['coach'] or session['admin']):
		return render_template('editathlete.html')
	else:
		return main()


@app.route('/editAth' , methods = ['GET', 'POST'])
def editAth():
	numOfColumns = 1
	athleteId = request.form['AthleteId']
	name = request.form['Name']
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT name, sport from Athletes where athleteId ='" + athleteId + "' and Name = '" + name +"'")
	data = cursor.fetchone()
	if data is None:
		print(data)
		return editathlete()
	else:
		stats = []
		stats.append(data[0]) 	#athelete name 
		stats.append(data[1])	#sport played 


		sportPlayed = data[1] + "stats"
		print(sportPlayed)
		cursor.execute("SELECT * from " + sportPlayed + " where athleteId= '" + str(athleteId) +"'")
		data = cursor.fetchone()
		for elem in data:
			stats.append(elem)
		print(stats)


		
		return editAth2(stats)

@app.route('/editAth2' , methods = ['GET', 'POST'])
def editAth2(data):
	return render_template('editAth2.html', data = data)


@app.route('/editstat', methods = ['GET', 'POST'])
def editstat():


	name = request.form['Name']
	athleteId = request.form['AthleteId']
	col1 = request.form['Col1']
	col2 = request.form['Col2']
	col3 = request.form['Col3']
	sports = request.form['Sport']


	print("debugging")
	print(athleteId)
	print(str(sports))
	print(col1)

	sportPlayed = sports + "stats"
	conn = mysql.connect()
	cursor = conn.cursor()
	
	if(str(sports).lower() == "track"):
		cursor.execute("UPDATE " + sportPlayed + " SET 100PB ='" + col1 +"', Location ='" + col2 + "', Date = '" + col3 + "' WHERE AthleteId ='" + athleteId + "'" )
	elif(str(sports).lower() == "basketball"):
		cursor.execute("UPDATE " + sportPlayed + " SET PPG ='" + col1 +"', RPG ='" + col2 + "', GP = '" + col3 + "' WHERE AthleteId ='" + athleteId + "'" )
	elif(str(sports).lower() == "swimming"):
		cursor.execute("UPDATE " + sportPlayed + " SET BestSwimTime ='" + col1 +"', Location ='" + col2 + "', Date = '" + col3 + "' WHERE AthleteId ='" + athleteId + "'" )
	else:
		print("invalid sportname")
	
	data = cursor.fetchone()
	print(data)
	conn.commit()
	return editathlete()


@app.route('/coach')
def coach():
	if(session['coach']):
		global coach_ID
		
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * from athletes a1 where a1.coachId ='" + coach_ID + "'")
		res = cursor.fetchall()
		print(res)
		data = []

		for ath in res:
			print("athno: " + str(ath[0]))
			athId = str(ath[0])
			curSport = ath[5] + "stats"
			cursor.execute("SELECT * from " + curSport + " where athleteId ='" + athId + "'")
			res2 = cursor.fetchone()

			
			if(res2 == None):
				res2 = []
				for i in range(5):
					res2.append("N/A")

			res2 = list(res2)

			res2.append(ath[0])
			res2.append(ath[2])
			res2.append(ath[3])

			res2.append(ath[5])
			i = 0
			for entry in res2:
				if entry == None:
					res2[i] = "N/A"
				i+=1

			print("new res")
			print(res2)
			data.append(res2)
			global coach_data
			coach_data = data 
			


		return render_template('coach.html', data = data)
	else:
		return main()



@app.route('/coach_login', methods = ['GET', 'POST'])
def coach_login():
	global coach_ID
	coachId = request.form['CoachId']
	coach_ID = coachId
	password = request.form['Password']
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Coaches where coachId ='" + coachId + "' and Password = '" + password +"'")
	data = cursor.fetchone()
	if data is None:
		return main()
	else:
		session['coach'] = True
		return coach()



@app.route('/athlete_logout')
def athlete_logout():
	session['athlete'] = False
	return main() 

@app.route('/logout')
def logout():
	session['coach'] = False
	session['admin'] = False
	session['athlete'] = False

	return main()

@app.route('/coach_logout')
def coach_logout():
	session['coach'] = False
	return main() 



@app.route('/mycoaches')
def mycoaches():
	global ath_ID
	global coach_ID
	cursor = mysql.connect().cursor()
	print
	cursor.execute("SELECT c1.name, c1.ExpInYears, c1.sport, c1.contactno FROM coaches c1 WHERE c1.sport ='" + athlete_data[0] +"'")
	#cursor.execute("SELECT c1.name FROM coaches c1, athletes a1 WHERE a1.CoachId ='" + str(coach_ID) +"'")
	data = cursor.fetchall()
	print('testin')
	
	for row in data:
		for col in row:
			print(col)
	return render_template('mycoaches.html', data = data)


@app.route('/mystats')
def mystats():
	return render_template('athlete.html', data = athlete_data)


@app.route('/mytrainees')
def mytrainees():
	return render_template('mytrainees.html')

@app.route('/help')
def help():
	return render_template('help.html')


@app.route('/athlete')
def athlete(stats):
	global athlete_data
	global ath_ID
	global coach_ID
	if(session['athlete']):
		sportPlayed = stats[5]
		sportText = sportPlayed + 'stats'
		ath_ID = stats[0]
		athleteName = stats[2]
		coach_ID = stats[4]
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * from " + sportText +" WHERE AthleteId ='" + str(stats[0]) +"'")
		res = cursor.fetchone()
		data = []
		print(res)
		data.append(sportPlayed)

		if(res is None):
			for i in range(1,6):
				data[i] = "N/A"
			data.append(athleteName)
			data.append('No Coach')

			return render_template('athlete.html', data = data)

		for i in range(len(res)):
			if(i>1):
				print(res[i])
				data.append(res[i])

		data.append(athleteName)
		athlete_data = res
		athlete_data = list(athlete_data)
		athlete_data.append(stats[5])
		athlete_data.append(athleteName)
		print('athletedata')
		print(athlete_data)

		cursor.execute("SELECT name from coaches WHERE CoachId ='" + str(coach_ID) +"'")
		res = cursor.fetchone()
		print('coach weher u at')
		print(res)
		if(res is None):
			athlete_data = res
			athlete_data.append(stats[5])

			return render_template('athlete.html', data = athlete_data)

		data.append(res[0])

		return render_template('athlete.html', data = athlete_data)
	else:
		return main()

@app.route('/athlete_login', methods = ['GET', 'POST'])
def athlete_login():
	athleteId = request.form['AthleteId']
	password = request.form['Password']
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Athletes where AthleteId ='" + athleteId + "' and Password = '" + password +"'")
	data = cursor.fetchone()
	print("ayyy", file = sys.stderr)
	print(data, file = sys.stderr)
	if data is None:
		return main()
	else:
		session['athlete'] = True
		return athlete(data)

@app.route('/addAthlete', methods = ['GET', 'POST'])
def addAthlete():
	if(session['coach'] or session['admin']):
		return render_template('addAthlete.html')
	else:
		return main()

@app.route('/delAthlete', methods = ['GET', 'POST'])
def delAthlete():
	if(session['coach'] or session['admin']):
		return render_template('delAthlete.html')
	else:
		return main()


@app.route('/emptyresult')
def emptyresult():
	return render_template('emptyresult.html')


@app.route('/addAth', methods =['GET', 'POST'])
def addAth():
	global coach_ID
	name = request.form['Name']
	password = request.form['Password']
	weight = request.form['Weight']
	sport = request.form['Sport']

	adminId =  "1"
	sportPlayed = sport + "stats"
	print(coach_ID)
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("INSERT into athletes(Password, Name, Weight, CoachId, Sport) VALUES ('"+ password +"', '"+ name +"', '"+weight+"', "+ str(coach_ID) +", '" + sport +"')")
	data = cursor.fetchone()
	conn.commit()
	cursor.execute("SELECT athleteId from Athletes where Password ='" + password + "' and Sport ='" + sport + "' and Weight ='" + weight + "' and Name = '" + name +"'")
	data = cursor.fetchone()
	athleteId = str(data[0])

	data = cursor.execute("INSERT into " + sportPlayed + "(AthleteId, AdminId) VALUES ("+ athleteId +"," + adminId +")")
	conn.commit()
	
	print(data)

	if(data == None):
		return addSuccess()
	return addAthlete()

@app.route('/addSuccess')
def addSuccess():
	return render_template('addsuccess.html')

@app.route('/delAth' , methods = ['GET', 'POST'])
def delAth():
	numOfColumns = 1
	athleteId = request.form['AthleteId']
	name = request.form['Name']
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT name, sport from Athletes where athleteId ='" + athleteId + "' and Name = '" + name +"'")
	data = cursor.fetchone()
	if data is None:
		print(data)
		return emptyresult()

	else:
		stats = []
		stats.append(data[0]) 	#athelete name 
		stats.append(data[1])	#sport played 

		conn = mysql.connect()
		cursor = conn.cursor()
		sportPlayed = data[1] + "stats"
		print(sportPlayed)
		cursor.execute("DELETE from " + sportPlayed + " where athleteId= '" + str(athleteId) +"'")
		conn.commit()
		cursor.execute("DELETE from athletes where athleteId= '" + str(athleteId) +"'")
		conn.commit()


		return delsuccess()

@app.route('/addAthlete_admin')
def addAthlete_admin():
	return render_template('addAthlete_admin.html')
		
@app.route('/addCoach_admin')
def addCoach_admin():
	return render_template('addCoach.html')

@app.route('/addAth_adm', methods =['GET', 'POST'])
def addAthA():
	
	name = request.form['Name']
	password = request.form['Password']
	weight = request.form['Weight']
	sport = request.form['Sport']
	coachId = request.form['CoachId']
	global admin_ID
	sportPlayed = sport + "stats"
	print(coach_ID)
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("INSERT into athletes(Password, Name, Weight, CoachId, Sport) VALUES ('"+ password +"', '"+ name +"', '"+weight+"', "+ str(coachId) +", '" + sport +"')")
	data = cursor.fetchone()
	conn.commit()
	cursor.execute("SELECT athleteId from Athletes where Password ='" + password + "' and Sport ='" + sport + "' and Weight ='" + weight + "' and Name = '" + name +"'")
	data = cursor.fetchone()
	athleteId = str(data[0])

	data = cursor.execute("INSERT into " + sportPlayed + "(AthleteId, AdminId) VALUES ("+ athleteId +"," + admin_ID +")")
	conn.commit()
	
	print(data)

	if(data == None):
		return "Error inserting data!"
	return athlete_admin()

@app.route('/addCoach', methods =['GET', 'POST'])
def addCoach():
	name = request.form['Name']
	orgId = request.form['OrgId']
	exp = request.form['ExpInYears']
	sport = request.form['Sport']
	password = request.form['Password']
	contactno = request.form['Contactno']




	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("INSERT into coaches(Password, Name, orgId , ExpInYears, Sport, contactno) VALUES ('"+ password +"', '"+ name +"', '"+orgId+"', '"+ exp +"', '" + sport +"','" + contactno + "')")
	data = cursor.fetchone()
	conn.commit()

	return addCoach_admin()

@app.route('/delCoach_admin', methods = ['GET', 'POST'])
def delCoach_admin():
	if(session['admin']):
		return render_template('delCoach_admin.html')
	else:
		return main()


@app.route('/delAthlete_admin', methods = ['GET', 'POST'])
def delAthlete_admin():
	if(session['admin']):
		return render_template('delAthlete_admin.html')
	else:
		return main()


@app.route('/delAthC' , methods = ['GET', 'POST'])
def delAthC():
	athleteId = request.form['AthleteId']
	name = request.form['Name']
	cursor = mysql.connect().cursor()
	cursor.execute("DELETE from athletes where athleteId= '" + str(athleteId) +"'")
	data = cursor.fetchone()
	conn.commit()

	return delAthlete_admin()


@app.route('/delAthA' , methods = ['GET', 'POST'])
def delAthA():
	numOfColumns = 1
	athleteId = request.form['AthleteId']
	name = request.form['Name']
	cursor = mysql.connect().cursor()
	cursor.execute("DELETE from coaches where coachId= '" + str(athleteId) +"'")
	data = cursor.fetchone()
	conn.commit()

	return delCoach_admin()

@app.route('/delsuccess')
def delsuccess():
	return render_template('delsuccess.html')
if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run()