from flask import Flask, render_template, request, session
from flaskext.mysql import MySQL
import os 

mysql = MySQL()
app = Flask(__name__); 





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
   
		

@app.route("/blah")
def blah():
	return render_template('index.html')

@app.route("/logout")
def logout():
	session['ath_in'] = False
	return main()

@app.route("/Auth")
def Authenticate():
	username = request.args.get('UserName')
	password = request.args.get('Password')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Users where Username='" + username + "' and Password = '" + password +"'")
	data = cursor.fetchone()
	if data is None:
		return main()
	else:
		session['ath_in'] = True
		return "Logged in succesfully"


@app.route('/admin')
def admin():
	if(session['admin']):
		return render_template('index.html')
	else:
		return main()



@app.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
	adminId = request.args.get('adminId')
	password = request.args.get('Password')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Admins where adminId ='" + adminId + "' and Password = '" + password +"'")
	if data is None:
		return main()
	else:
		session['admin'] = True
		return admin()
	
@app.route('admin_logoff')
def admin_logoff():
	session['admin'] = False
	return main() 


@app.route('coach')
def coach():
	if(session['coach']):
		return render_template('coach.html')
	else:
		return main()



@app.route('/coach_login', methods = ['GET', 'POST'])
def coach_login():
	coachId = request.args.get('coachId')
	password = request.args.get('Password')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Coaches where coachId ='" + adminId + "' and Password = '" + password +"'")
	if data is None:
		return main()
	else:
		session['coach'] = True
		return coach()



@app.route('/athlete_logout')
def coach_logout():
	session['athlete'] = False
	return main() 

@app.route('/coach_logout')
	session['coach'] = False
	return main() 

@app.route('/athlete')
def athlete():
	if(session['athlete']):
		return render_template('athlete.html')
	else:
		return main()

@app.route('/athlete_login', methods = ['GET', 'POST'])
def athlete_login():
 	athleteId = request.args.get('athleteId')
	password = request.args.get('Password')
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from Athletes where athleteId ='" + adminId + "' and Password = '" + password +"'")
	if data is None:
		return main()
	else:
		session['athlete'] = True
		return athlete()
 	"""
 	if 'ath_user' in session:
 		return redirect(url_for('ath_dashboard'))

 	error = None;
 	try:
 		if request.method == 'POST':
 			athname_form = request.form['ath_name']
 		"""
if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run()