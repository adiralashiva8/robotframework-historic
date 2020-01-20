from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'world'

mysql = MySQL(app)

@app.route('/rfhistoric', methods=['GET'])
def index():

   cursor = mysql.connection.cursor()
   cursor.execute("SELECT Name, CountryCode, Population FROM city LIMIT 10;")
   records = cursor.fetchall()

   return render_template('city.html', result=records, content_type='application/json')

@app.route('/rfhistoric/test', methods=['GET'])
def test():
   return render_template('index.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug=True)