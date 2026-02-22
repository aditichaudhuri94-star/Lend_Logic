import os
import MySQLdb.cursors  # Fixes "MySQLdb is not defined" error
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from utils import calculate_emi, check_eligibility

# Load variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database Config
app.config['MYSQL_HOST'] = os.getenv("DB_HOST")
app.config['MYSQL_USER'] = os.getenv("DB_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("DB_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("DB_NAME")

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
                       (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect('/')
    return render_template("register.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['role'] = user['role']
        if user['role'] == 'admin':
            return redirect('/admin')
        return redirect('/dashboard')

    flash("Invalid Credentials")
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect('/')
    return render_template("dashboard.html")

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if 'user_id' not in session: return redirect('/')
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate'])
        tenure = int(request.form['tenure'])
        income = float(request.form['income'])

        emi, total, schedule = calculate_emi(principal, rate, tenure)
        eligibility = check_eligibility(emi, income)

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO loans(user_id, principal, interest_rate, tenure, emi, total_payment, eligibility)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (session['user_id'], principal, rate, tenure, emi, total, eligibility))
        mysql.connection.commit()
        cursor.close()

        return render_template("schedule.html", emi=emi, total=total, 
                               eligibility=eligibility, schedule=schedule)
    return render_template("apply_loan.html")

@app.route('/admin')
def admin():
    if session.get('role') != 'admin': return redirect('/dashboard')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM loans")
    loans = cursor.fetchall()
    cursor.close()

    total = len(loans)
    approved = len([l for l in loans if l['eligibility'] == 'Eligible'])
    rejected = total - approved
    return render_template("admin_dashboard.html", loans=loans, total=total, 
                           approved=approved, rejected=rejected)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)