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


@app.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
	return -1		


@app.route('/coach_login', methods = ['GET', 'POST'])
def coach_login():
	return -1

@app.route('/athlete_login', methods = ['GET', 'POST'])
def athlete_login():
 	return ""
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