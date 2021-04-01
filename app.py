from flask import Flask, request, render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
database = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'secret_go_brr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'


@app.route('/')
def index():
	if not session.get("logged"):
		return redirect(url_for("login"))
	return render_template('index.html')

@app.route('/login', methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session["logged"] = True
	return render_template('login.html')

@app.route('/register')
def register():
	if request.method == "POST":
		fname = request.data['fullname']
		username = request.data['username']
		password = request.data["password"]
	return render_template('register.html')


if __name__ == "__main__":
	app.run(debug=True, port=5500)
