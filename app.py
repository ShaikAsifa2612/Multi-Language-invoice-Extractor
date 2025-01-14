from flask import Flask, render_template, request, redirect, url_for, flash
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
    print("Index route accessed")
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    print("Register route accessed")
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        mysql.connection.commit()
        flash("Registration successful!", "success")
    except MySQLdb.MySQLError as e:
        print(f"Error: {e}")
        mysql.connection.rollback()
        flash("Registration failed, please try again.", "error")
    finally:
        cursor.close()
    
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    print("Login route accessed")
    username_email = request.form['username-email']
    password = request.form['password']
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE (username = %s OR email = %s) AND password = %s', (username_email, username_email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        print("Login Successful")
        flash("Login successful!", "success")
        return redirect(url_for('success'))  # Redirect to success page after login
    else:
        flash("Invalid credentials, please try again.", "error")
        return redirect(url_for('index'))  # Redirect back to index with an error message

@app.route('/success')



def success():
   
    os.environ["BROWSER"] = "none"
    # Directly execute the Streamlit app
    try:
        subprocess.run(["streamlit", "run", "app1.py"], check=True)
    except subprocess.CalledProcessError as e:
        # Handle any error if the Streamlit app fails to execute
        print(f"Error occurred while running Streamlit app: {e}")



#def success():
 #
 #   return "<h1 style='color:red;'>Welcome, you have logged in successfully!</h1>"

if __name__ == '__main__':
    app.run(debug=True, port=5001)