from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import config
from .args import parse_options

app = Flask(__name__, template_folder='templates')

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redirect')
def redirect_url():
    return render_template('redirect.html')

@app.route('/home', methods=['GET'])
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("select table_schema from information_schema.tables group by table_schema order by create_time;")
    data = cursor.fetchall()
    return render_template('home.html', data=data)

@app.route('/<db>/delete', methods=['GET'])
def delete_db(db):
    cursor = mysql.connection.cursor()
    cursor.execute("DROP DATABASE %s;" % db)
    return redirect(url_for('home'))

@app.route('/newdb', methods=['GET', 'POST'])
def add_db():
    if request.method == "POST":
        db_name = request.form['dbname']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("Create DATABASE IF NOT EXISTS %s;" % db_name)
            use_db(cursor, db_name)
            cursor.execute("CREATE TABLE IF NOT EXISTS results(ID int not null auto_increment primary key, DATE text, NAME text, TOTAL int, PASSED int, FAILED int, TIME int)") 
            cursor.execute("CREATE TABLE IF NOT EXISTS test_results(ID int, TESTCASE text, STATUS text, TIME int, MESSAGE text)") 
            mysql.commit()
        except Exception:
            print(Exception)

        finally:
            return redirect(url_for('home'))
    else:
        return render_template('newdb.html')

@app.route('/<db>/dashboard', methods=['GET'])
def dashboard(db):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)

    cursor.execute("SELECT COUNT(ID) from results;")
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(ID) from test_results;")
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT PASSED, FAILED, TOTAL from results order by ID desc LIMIT 1;")
        last_exe_pie_data = cursor.fetchall()

        cursor.execute("SELECT SUM(PASSED), SUM(FAILED), SUM(TOTAL), COUNT(ID) from (SELECT PASSED, FAILED, TOTAL, ID from results order by ID desc LIMIT 10) AS T;")
        last_ten_exe_pie_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(PASSED),2), ROUND(AVG(TIME),2), COUNT(ID) from (SELECT PASSED, TIME, ID from results order by ID desc LIMIT 10) AS T;")
        last_ten_exe_avg_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(PASSED),2), ROUND(AVG(TIME),2) from results;")
        over_all_exe_avg_data = cursor.fetchall()

        cursor.execute("SELECT SUM(PASSED), SUM(FAILED), SUM(TOTAL), COUNT(ID) from results order by ID desc;")
        over_all_exe_pie_data = cursor.fetchall()

        cursor.execute("SELECT ID, PASSED, FAILED, TIME from results order by ID desc LIMIT 10;")
        last_ten_data = cursor.fetchall()

        return render_template('dashboard.html', last_ten_data=last_ten_data,
        last_exe_pie_data=last_exe_pie_data,
        last_ten_exe_pie_data=last_ten_exe_pie_data,
        over_all_exe_pie_data=over_all_exe_pie_data,
        last_ten_exe_avg_data=last_ten_exe_avg_data,
        over_all_exe_avg_data=over_all_exe_avg_data, db_name=db)
    
    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/ehistoric', methods=['GET'])
def ehistoric(db):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    cursor.execute("SELECT * from results order by ID desc LIMIT 500;")
    data = cursor.fetchall()
    return render_template('ehistoric.html', data=data, db_name=db)

@app.route('/<db>/tmetrics', methods=['GET'])
def tmetrics(db):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    # Get last row execution ID
    cursor.execute("SELECT ID from results order by ID desc LIMIT 1;")
    data = cursor.fetchone()
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from test_results WHERE ID=%s;" % data)
    data = cursor.fetchall()
    return render_template('tmetrics.html', data=data, db_name=db)

@app.route('/<db>/search', methods=['GET', 'POST'])
def search(db):
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, db)
        cursor.execute("SELECT * from test_results WHERE TESTCASE LIKE '%{name}%' OR STATUS LIKE '%{name}%' OR ID LIKE '%{name}%' ORDER BY ID DESC LIMIT 10000;".format(name=search))
        data = cursor.fetchall()
        return render_template('search.html', data=data, db_name=db)
    else:
        return render_template('search.html', db_name=db)

def use_db(cursor, db_name):
    cursor.execute("USE %s;" % db_name)

def main():

    args = parse_options()

    app.config['MYSQL_HOST'] = args.sqlhost
    app.config['MYSQL_USER'] = args.username
    app.config['MYSQL_PASSWORD'] = args.password

    app.run(host=args.apphost)