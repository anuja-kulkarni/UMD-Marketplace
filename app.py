from flask import Flask, render_template, request, redirect, url_for, session, flash
from flaskext.mysql import MySQL
import re
from datetime import timedelta

app = Flask(__name__)
mysql = MySQL()

#setting secret key to use session to store user data
app.secret_key = 'marketplace_secret_key'
#Below setting helps hold items in cart for up to 3 days
app.permanent_session_lifetime = timedelta(days=3)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root12345'
app.config['MYSQL_DATABASE_DB'] = 'umd_marketplace'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        userName = request.form['userName']
        email = request.form['email']
        password = request.form['password']
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("insert into user (name,userName,email,password) values (%s,%s,%s,%s)", (name,userName,email,password))
        conn.commit()
    return render_template('signup.html')


@app.route('/shop', methods = ['GET','POST'])
def shop():
    if "user" in session:
        user = session["user"]
        items = [
        {"name": "Item 1", "description": "Description for Item 1","price":"$250", "image": "https://via.placeholder.com/150"},
        {"name": "Item 2", "description": "Description for Item 2", "image": "https://via.placeholder.com/150","price":"$350"},
        {"name": "Item 3", "description": "Description for Item 3", "image": "https://via.placeholder.com/150","price":"$250"},
        {"name": "Item 4", "description": "Description for Item 4", "image": "https://via.placeholder.com/150","price":"$150"},
        {"name": "Item 5", "description": "Description for Item 5", "image": "https://via.placeholder.com/150","price":"$50"}
    ]
        return render_template('shop/shop.html', items=items)
    else:
        return redirect(url_for("login"))

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    password_entered = ''
    user = None
    if request.method == 'POST':
        session.permanent = True
        username = request.form['userName']
        password_entered = request.form['password']
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM user WHERE userName = %s', (username,))
        user = cursor.fetchone()  
        if user == None:
            return render_template('login.html')
        session['user'] = username
        return redirect(url_for("shop"))
    else:
        if "user" in session and user:
            if password_entered == user[4]:
                session['loggedin'] = True
                flash('Logged in successfully!')
                return redirect(url_for("shop"))
        return render_template('login.html')

@app.route('/orderhistory')
def orderhistory():
    return render_template('orderhistory/orderhistory.html')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart/cart.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

