import bcrypt
from app import db

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
        
