from flask import Flask, request, render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
database = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'secret_go_brr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite3'

class Users(database.Model):
	id = database.Column(database.Integer, primary_key=True)
	fname = database.Column(database.String(64))
	uname = database.Column(database.String(64), unique=True)
	password = database.Column(database.String(64))

	def __init__(self, fname, uname, password):
		self.fname = fname
		self.uname = uname
		self.password = password

class Questions(database.Model):
	id = database.Column(database.Integer, primary_key=True)
	user = database.Column(database.String(64))
	question = database.Column(database.String(1024))
	no_answ = database.Column(database.Integer)

	def __init__(self, user, question):
		self.user = user
		self.question = question
		no_answ = 0

class Answers(database.Model):
	id = database.Column(database.Integer, primary_key=True)
	qid = database.Column(database.Integer)
	user = database.Column(database.String(64))
	answer = database.Column(database.String(1024000))

	def __init__(self, qid, user, answer):
		self.qid = qid
		self.user = user
		self.answer = answer

@app.route('/')
def index():
	if not session.get("logged"):
		return redirect(url_for("login"))
	questions = Questions.query.all()
	final = []
	for i in range(len(questions) - 1, -1, -1):
		final.append(questions[i])
	return render_template('index.html', question=final)

@app.route('/login', methods=["POST", "GET"])
def login():
	message = ""
	if request.method == "POST":
		username = request.form["username"]
		passw = request.form["password"]
		user = Users.query.filter_by(uname=username).first()
		if not user:
			message = "User doesn't exist"
		elif user.password != passw:
			message = "Password doesn't match"
		else:
			session["logged"] = True
			session["user"] = user.uname
			return redirect("/")

	return render_template('login.html', message=message)

@app.route('/register', methods=["POST", "GET"])
def register():
	message = ""
	if request.method == "POST":
		fname = request.form['fullname']
		username = request.form['username']
		password = request.form["password"]
		previous = Users.query.filter_by(uname=username).first()
		if previous:
			message = "User already exists"
		else:
			user = Users(fname, username, password)
			database.session.add(user)
			database.session.commit()
			message = "Sucessfully Registered"
	return render_template('register.html', message=message)

@app.route('/post', methods=["POST"])
def post():
	question = request.form["question"]
	uname = session["user"]
	quest = Questions(uname, question)
	database.session.add(quest)
	database.session.commit()
	return redirect('/')


@app.route('/question/<int:id>', methods=["GET", "POST"])
def question(id):
	if request.method == "POST":
		answer = request.form["answer"]
		user = session["user"]
		ans = Answers(id, user, answer)
		database.session.add(ans)
		database.session.commit()
	question = Questions.query.filter_by(id=id).first()
	answers = Answers.query.filter_by(qid=id)
	final = []
	for i in range(answers.count() - 1, -1, -1):
		final.append(answers[i])
	return render_template('answer.html', question=question, answers=final)

@app.route("/logout")
def logout():
	session["logged"] = False


if __name__ == "__main__":
	database.create_all()
	app.run(debug=True, port=5500)
