from flask import render_template, request, redirect, session, url_for
from models import User, Subscribe_stock
from app import db, app
import requests
import os
import plotly.graph_objs as go
from datetime import datetime

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
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect('/login')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        stock_symbol = 'IBM'
        if request.method == 'POST':
            stock_symbol = request.form['stock']
            
            graphJSON = get_stock_data(stock_symbol)
            return render_template('./dashboard.html', graphJSON=graphJSON, stock_symbol=stock_symbol)

        graphJSON = get_stock_data(stock_symbol)
        return render_template('./dashboard.html', graphJSON=graphJSON, stock_symbol=stock_symbol)
    else:
        return redirect('/login')
    
@app.route('/dashboard/subscribe', methods=['GET', 'POST'])
def dashboard_subscribe():
    if 'username' in session:
        if request.method == 'POST':
            stock_symbol = request.form['stock']
            user = User.query.filter_by(email=session['email']).first()
            new_subscription = Subscribe_stock(stock_symbol=stock_symbol, user_id=user.id)
            
            # return true if alredy exist else false
            if new_subscription.check_already_subscribed(stock_symbol, user.id):
                return redirect('/dashboard', error="Already subscribed")
            else:
                db.session.add(new_subscription)
                db.session.commit()
            
        return redirect('/dashboard')
        
    else:
        return redirect('/login')

@app.route('/dashboard/unsubscribe/<stock_symbol>', methods=['GET', 'POST'])
def dashboard_unsubscribe(stock_symbol):
    if 'username' in session:
        print(stock_symbol)
        user = User.query.filter_by(email=session['email']).first()
        subscription = Subscribe_stock.query.filter_by(stock_symbol=stock_symbol, user_id=user.id).first()
        print(subscription)
        db.session.delete(subscription)
        db.session.commit()
        return redirect('/dashboard/watchlist')
    else:
        return redirect('/login')

@app.route('/dashboard/watchlist', methods=['GET', 'POST'])
def user_watchlist():
    if 'username' in session:
        user = User.query.filter_by(email=session['email']).first()
        stock_list = Subscribe_stock.query.filter_by(user_id=user.id).all()
        return render_template('./watchlist.html', stock_list=stock_list)
    else:
        return redirect('/login')

def get_stock_data(stock_symbol):
        api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey={os.environ.get("API_KEY")}'
        # api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey=demo'
        try:
            response = requests.get(api_url)
            data = response.json()['Time Series (5min)']
            print("Data: ", data)
            timestamps = [datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') for timestamp in data.keys()]
            closing_prices = [float(entry['4. close']) for entry in data.values()]

            plotly_fig = go.Figure()

            # Add trace
            plotly_trace = go.Scatter(x=timestamps, y=closing_prices, mode='lines+markers', name='Closing Price')
            plotly_fig.add_trace(plotly_trace)

            # Layout adjustments
            plotly_fig.update_layout(
                title=f'{stock_symbol} Stock Price (5min intervals)',
                xaxis_title='Timestamp',
                yaxis_title='Closing Price'
            )

            # Create graphJSON
            graphJSON = plotly_fig.to_json()

            return graphJSON
        except Exception as e:
            return render_template('/login.html', error="sorry something went wrong, please try again later.")
