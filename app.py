from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class User(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(80), unique=True, nullable=False)
# 	email = db.Column(db.String(120), unique=True, nullable=False)
# 	password = db.Column(db.String(120), nullable=False)

# 	def __repr__(self):
# 		return '<User %r>' % self.id

@app.route('/')
def register(name=None):
	# return render_template('register.html', name=name)
	return 'Hello, World!'

@app.route('/login')
def login(name=None):
	return render_template('./login.html', name=name)
