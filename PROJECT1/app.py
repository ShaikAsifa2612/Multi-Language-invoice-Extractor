from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb
import subprocess
import os

app = Flask(__name__)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Team7JNTU4Year'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'trail6'  # Database name

mysql = MySQL(app)
app.secret_key = 'your_secret_key'  # For flashing messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        return jsonify({"status": "error", "message": "Passwords do not match. Please try again."})
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        return jsonify({"status": "success", "message": "Registration successful!"})
    except MySQLdb.IntegrityError as e:
        if e.args[0] == 1062:  # Duplicate entry error code
            return jsonify({"status": "error", "message": "Username already exists. Please choose a different username."})
        else:
            return jsonify({"status": "error", "message": "Registration failed, please try again."})
    finally:
        cursor.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({"status": "success", "message": "Login successful!"})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials, please try again."})

@app.route('/success')
def success():
    os.environ["BROWSER"] = "none"
    # Directly execute the Streamlit app
    try:
        subprocess.run(["streamlit", "run", "app1.py"], check=True)
    except subprocess.CalledProcessError as e:
        # Handle any error if the Streamlit app fails to execute
        print(f"Error occurred while running Streamlit app: {e}")

if __name__ == '__main__':
    app.run()