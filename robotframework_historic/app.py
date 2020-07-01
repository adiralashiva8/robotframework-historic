from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import config
from .args import parse_options

app = Flask(__name__, template_folder='templates')

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/redirect')
def redirect_url():
    return render_template('redirect.html')

@app.route('/home', methods=['GET'])
def home():
    cursor = mysql.connection.cursor()
    use_db(cursor, "robothistoric")
    cursor.execute("SELECT * FROM TB_PROJECT;")
    data = cursor.fetchall()
    return render_template('home.html', data=data)

@app.route('/<db>/deldbconf', methods=['GET'])
def delete_db_conf(db):
    return render_template('deldbconf.html', db_name = db)

@app.route('/<db>/delete', methods=['GET'])
def delete_db(db):
    cursor = mysql.connection.cursor()
    cursor.execute("DROP DATABASE %s;" % db)
    # use_db(cursor, "robothistoric")
    cursor.execute("DELETE FROM robothistoric.TB_PROJECT WHERE Project_Name='%s';" % db)
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/newdb', methods=['GET', 'POST'])
def add_db():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        db_image = request.form['dbimage']
        cursor = mysql.connection.cursor()

        try:
            # create new database for project
            cursor.execute("Create DATABASE %s;" % db_name)
            # update created database info in robothistoric.TB_PROJECT table
            cursor.execute("INSERT INTO robothistoric.TB_PROJECT ( Project_Id, Project_Name, Project_Desc, Project_Image, Created_Date, Last_Updated, Total_Executions, Recent_Pass_Perc, Overall_Pass_Perc) VALUES (0, '%s', '%s', '%s', NOW(), NOW(), 0, 0, 0);" % (db_name, db_desc, db_image))
            # create tables in created database
            use_db(cursor, db_name)
            cursor.execute("Create table TB_EXECUTION ( Execution_Id INT NOT NULL auto_increment primary key, Execution_Date DATETIME, Execution_Desc TEXT, Execution_Total INT, Execution_Pass INT, Execution_Fail INT, Execution_Time FLOAT, Execution_STotal INT, Execution_SPass INT, Execution_SFail INT);")
            cursor.execute("Create table TB_SUITE ( Suite_Id INT NOT NULL auto_increment primary key, Execution_Id INT, Suite_Name TEXT, Suite_Status CHAR(4), Suite_Total INT, Suite_Pass INT, Suite_Fail INT, Suite_Time FLOAT);")
            cursor.execute("Create table TB_TEST ( Test_Id INT NOT NULL auto_increment primary key, Execution_Id INT, Test_Name TEXT, Test_Status CHAR(4), Test_Time FLOAT, Test_Error TEXT, Test_Comment TEXT);")
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('home'))
    else:
        return render_template('newdb.html')

@app.route('/<db>/dashboard', methods=['GET'])
def dashboard(db):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)

    cursor.execute("SELECT COUNT(Execution_Id) from TB_EXECUTION;")
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Suite_Id) from TB_SUITE;")
    suite_results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Test_Id) from TB_TEST;")
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and suite_results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT Execution_Pass, Execution_Fail, Execution_Total, Execution_Time from TB_EXECUTION order by Execution_Id desc LIMIT 1;")
        last_exe_pie_data = cursor.fetchall()

        cursor.execute("SELECT SUM(Execution_Pass), SUM(Execution_Fail), SUM(Execution_Total), COUNT(Execution_Id) from (SELECT Execution_Pass, Execution_Fail, Execution_Total, Execution_Id from TB_EXECUTION order by Execution_Id desc LIMIT 10) AS T;")
        last_ten_exe_pie_data = cursor.fetchall()

        cursor.execute("SELECT SUM(Execution_Pass), SUM(Execution_Fail), SUM(Execution_Total), COUNT(Execution_Id) from TB_EXECUTION order by Execution_Id desc;")
        over_all_exe_pie_data = cursor.fetchall()

        cursor.execute("SELECT Execution_Id, Execution_Pass, Execution_Fail, Execution_Time from TB_EXECUTION order by Execution_Id desc LIMIT 10;")
        last_ten_data = cursor.fetchall()

        cursor.execute("select execution_pass, ROUND(MIN(execution_pass),2), ROUND(AVG(execution_pass),2), ROUND(MAX(execution_pass),2) from TB_EXECUTION order by execution_id desc;")
        execution_pass_data = cursor.fetchall()

        cursor.execute("select execution_fail, ROUND(MIN(execution_fail),2), ROUND(AVG(execution_fail),2), ROUND(MAX(execution_fail),2) from TB_EXECUTION order by execution_id desc;")
        execution_fail_data = cursor.fetchall()

        cursor.execute("select execution_time, ROUND(MIN(execution_time),2), ROUND(AVG(execution_time),2), ROUND(MAX(execution_time),2) from TB_EXECUTION order by execution_id desc;")
        execution_time_data = cursor.fetchall()

        return render_template('dashboard.html', last_ten_data=last_ten_data,
        last_exe_pie_data=last_exe_pie_data,
        last_ten_exe_pie_data=last_ten_exe_pie_data,
        over_all_exe_pie_data=over_all_exe_pie_data,
        execution_pass_data=execution_pass_data,
        execution_fail_data=execution_fail_data,
        execution_time_data=execution_time_data,db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/ehistoric', methods=['GET'])
def ehistoric(db):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    cursor.execute("SELECT * from TB_EXECUTION order by Execution_Id desc LIMIT 500;")
    data = cursor.fetchall()
    return render_template('ehistoric.html', data=data, db_name=db)

@app.route('/<db>/deleconf/<eid>', methods=['GET'])
def delete_eid_conf(db, eid):
    return render_template('deleconf.html', db_name = db, eid = eid)

@app.route('/<db>/edelete/<eid>', methods=['GET'])
def delete_eid(db, eid):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    # remove execution from tables: execution, suite, test
    cursor.execute("DELETE FROM TB_EXECUTION WHERE Execution_Id='%s';" % eid)
    cursor.execute("DELETE FROM TB_SUITE WHERE Execution_Id='%s';" % eid)
    cursor.execute("DELETE FROM TB_TEST WHERE Execution_Id='%s';" % eid)
    # get latest execution info
    cursor.execute("SELECT Execution_Pass, Execution_Total from TB_EXECUTION ORDER BY Execution_Id DESC LIMIT 1;")
    data = cursor.fetchall()
    # get no. of executions
    cursor.execute("SELECT COUNT(*) from TB_EXECUTION;")
    exe_data = cursor.fetchall()

    try:
        if data[0][0] > 0:
            recent_pass_perf = float("{0:.2f}".format((data[0][0]/data[0][1]*100)))
        else:
            recent_pass_perf = 0
    except:
        recent_pass_perf = 0

    # update robothistoric project
    cursor.execute("UPDATE robothistoric.TB_PROJECT SET Total_Executions=%s, Last_Updated=now(), Recent_Pass_Perc=%s WHERE Project_Name='%s';" % (int(exe_data[0][0]), recent_pass_perf, db))
    # commit changes
    mysql.connection.commit()
    return redirect(url_for('ehistoric', db = db))

@app.route('/<db>/tmetrics', methods=['GET', 'POST'])
def tmetrics(db):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    if request.method == "POST":
        textField = request.form['textField']
        rowField = request.form['rowField']
        cursor.execute("Update TB_TEST SET Test_Comment='%s' WHERE Test_Id=%s;" % (str(textField), str(rowField)))
        mysql.connection.commit()

    # Get last row execution ID
    cursor.execute("SELECT Execution_Id from TB_EXECUTION order by Execution_Id desc LIMIT 1;")
    data = cursor.fetchone()
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from TB_TEST WHERE Execution_Id=%s;" % data)
    data = cursor.fetchall()
    return render_template('tmetrics.html', data=data, db_name=db)

@app.route('/<db>/metrics/<eid>', methods=['GET'])
def metrics(db, eid):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    # Get testcase results of execution id
    cursor.execute("SELECT * from TB_TEST WHERE Execution_Id=%s;" % eid)
    test_data = cursor.fetchall()
    # get suite results of execution id
    cursor.execute("SELECT * from TB_SUITE WHERE Execution_Id=%s;" % eid)
    suite_data = cursor.fetchall()
    # get project image
    cursor.execute("SELECT Project_Image from robothistoric.TB_PROJECT WHERE Project_Name='%s';" % db)
    project_image = cursor.fetchall()
    # get execution info
    cursor.execute("SELECT * from TB_EXECUTION WHERE Execution_Id=%s;" % eid)
    exe_data = cursor.fetchall()
    return render_template('metrics.html', suite_data=suite_data, test_data = test_data, project_image= project_image[0][0], exe_data = exe_data)

@app.route('/<db>/tmetrics/<eid>', methods=['GET', 'POST'])
def eid_tmetrics(db, eid):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    if request.method == "POST":
        textField = request.form['textField']
        rowField = request.form['rowField']
        cursor.execute("Update TB_TEST SET Test_Comment='%s' WHERE Test_Id=%s;" % (str(textField), str(rowField)))
        mysql.connection.commit()

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from TB_TEST WHERE Execution_Id=%s;" % eid)
    data = cursor.fetchall()
    return render_template('eidtmetrics.html', data=data, db_name=db)

@app.route('/<db>/failures/<eid>', methods=['GET', 'POST'])
def eid_failures(db, eid):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    if request.method == "POST":
        textField = request.form['textField']
        rowField = request.form['rowField']
        cursor.execute("Update TB_TEST SET Test_Comment='%s' WHERE Test_Id=%s;" % (str(textField), str(rowField)))
        mysql.connection.commit()

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from TB_TEST WHERE Execution_Id=%s and Test_Status='FAIL';" % eid)
    data = cursor.fetchall()
    return render_template('failures.html', data=data, db_name=db)

@app.route('/<db>/search', methods=['GET', 'POST'])
def search(db):
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, db)
        cursor.execute("SELECT * from TB_TEST WHERE Test_Name LIKE '%{name}%' OR Test_Status LIKE '%{name}%' OR Execution_Id LIKE '%{name}%' ORDER BY Execution_Id DESC LIMIT 10000;".format(name=search))
        data = cursor.fetchall()
        return render_template('search.html', data=data, db_name=db)
    else:
        return render_template('search.html', db_name=db)

@app.route('/<db>/flaky', methods=['GET'])
def flaky(db):
    cursor = mysql.connection.cursor()
    use_db(cursor, db)
    cursor.execute("SELECT Execution_Id from ( SELECT Execution_Id from TB_EXECUTION ORDER BY Execution_Id DESC LIMIT 5 ) as tmp ORDER BY Execution_Id ASC LIMIT 1;")
    last_five = cursor.fetchall()
    cursor.execute("SELECT Execution_Id from TB_EXECUTION ORDER BY Execution_Id DESC LIMIT 5;")
    last_five_ids = cursor.fetchall()
    sql_query = "SELECT Execution_Id, Test_Name, Test_Status from TB_TEST WHERE Execution_Id >= %s ORDER BY Execution_Id DESC;" % (str(last_five[0][0]))
    cursor.execute(sql_query)
    data = cursor.fetchall()
    # print("==== Before Sorted Data ===")
    # print(data)
    sorted_data = sort_tests(data)
    # print("==== After Sorted Data ===")
    # print(sorted_data)
    return render_template('flaky.html', data=sorted_data, db_name=db, builds=last_five_ids)

@app.route('/<db>/compare', methods=['GET', 'POST'])
def compare(db):
    if request.method == "POST":
        eid_one = request.form['eid_one']
        eid_two = request.form['eid_two']
        cursor = mysql.connection.cursor()
        use_db(cursor, db)
        # fetch first eid tets results
        cursor.execute("SELECT Execution_Id, Test_Name, Test_Status, Test_Time, Test_Error from TB_TEST WHERE Execution_Id=%s;" % eid_one )
        first_data = cursor.fetchall()
        # fetch second eid test results
        cursor.execute("SELECT Execution_Id, Test_Name, Test_Status, Test_Time, Test_Error from TB_TEST WHERE Execution_Id=%s;" % eid_two )
        second_data = cursor.fetchall()
        # combine both tuples
        data = first_data + second_data
        sorted_data = sort_tests(data)
        return render_template('compare.html', data=sorted_data, db_name=db, fb = eid_one, sb = eid_two)
    else:
        return render_template('compare.html', db_name=db)

@app.route('/<db>/query', methods=['GET', 'POST'])
def query(db):
    if request.method == "POST":
        query = request.form['query']
        cursor = mysql.connection.cursor()
        use_db(cursor, db)
        try:
            cursor.execute("{name}".format(name=query))
            data = cursor.fetchall()
            return render_template('query.html', data=data, db_name=db)
        except Exception as e:
            print(str(e))
            return render_template('query.html', db_name=db)
    else:
        return render_template('query.html', db_name=db)

def use_db(cursor, db_name):
    cursor.execute("USE %s;" % db_name)

def sort_tests(data_list):
    out = {}
    for elem in data_list:
        try:
            out[elem[1]].extend(elem[2:])
        except KeyError:
            out[elem[1]] = list(elem)
    return [tuple(values) for values in out.values()]

def main():

    args = parse_options()

    app.config['MYSQL_HOST'] = args.sqlhost
    app.config['MYSQL_USER'] = args.username
    app.config['MYSQL_PASSWORD'] = args.password
    app.config['auth_plugin'] = 'mysql_native_password'

    app.run(host=args.apphost)
