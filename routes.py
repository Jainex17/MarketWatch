from flask import render_template, request, redirect, session
from models import User
from app import db, app

@app.route('/', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/dashboard')
    else:
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
    if 'username' in session:
        return redirect('/dashboard')
    else:
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
    if 'username' in session:
        # stock_symbol = 'IBM'

        # api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={os.environ.get("API_KEY")}'
        
        # response = requests.get(api_url)
        # data = response.json()['Time Series (5min)']
        # print(data)
     
        return render_template('./dashboard.html')
    else:
        return redirect('/login')

