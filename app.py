import os
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, enterpassword):
        stored_password_bytes = bytes(self.password)
        print('Stored Password Bytes', stored_password_bytes)
        return bcrypt.checkpw(enterpassword.encode('utf-8'), stored_password_bytes)
        
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and request.form['username'] and request.form['email'] and request.form['password']:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/login')
    else:
        return render_template('./register.html')
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('./login.html', error="Invalid email or password")

    return render_template('./login.html')

@app.route('/dashboard')
def dashboard():
    return "Dashboard"
