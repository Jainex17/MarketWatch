import bcrypt
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, enterpassword):
        stored_password_bytes = bytes(self.password)
        return bcrypt.checkpw(enterpassword.encode('utf-8'), stored_password_bytes)

class Subscribe_stock(db.Model):
    __tablename__ = 'subscribe_stock'
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, stock_symbol, user_id):
        self.stock_symbol = stock_symbol
        self.user_id = user_id

    def check_already_subscribed(self, stock_symbol, user_id):
        checkval = Subscribe_stock.query.filter_by(stock_symbol=stock_symbol, user_id=user_id).first()
        if checkval:
            return True
        else:  
            return False