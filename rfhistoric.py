from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from config import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USER_NAME
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DATABASE_NAME

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/shistoric', methods=['GET'])
def shistoric():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from results order by ID desc LIMIT 50;")
    data = cursor.fetchall()
    return render_template('shistoric.html', data=data)

@app.route('/tmetrics', methods=['GET'])
def tmetrics():
    cursor = mysql.connection.cursor()
    # Get last row execution ID
    cursor.execute("SELECT ID from results order by ID desc LIMIT 1;")
    data = cursor.fetchone()
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from test_results WHERE ID=%s;" % data)
    data = cursor.fetchall()
    return render_template('tmetrics.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from test_results WHERE TESTCASE LIKE '%{name}%' OR STATUS LIKE '%{name}%' OR ID LIKE '%{name}%' LIMIT 1000;".format(name=search))
        data = cursor.fetchall()
        return render_template('search.html', data=data)
    else:
        return render_template('search.html')

if __name__ == '__main__':
   app.run()