import datetime
import mysql.connector
from robot.libraries.BuiltIn import BuiltIn

class RfHistoricListener:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.PRE_RUNNER = 0
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_suite(self, name, attrs):        
        self.test_count = len(attrs['tests'])
        self.suite_name =  name

        # set-up database
        if self.PRE_RUNNER == 0:
            self.HOST = BuiltIn().get_variable_value("${HOST}")
            self.USER_NAME = BuiltIn().get_variable_value("${USER_NAME}")
            self.PASSWORD = BuiltIn().get_variable_value("${PASSWORD}")
            self.DATABASE_NAME = BuiltIn().get_variable_value("${DATABASE_NAME}")
            self.EXECUTION_NAME = BuiltIn().get_variable_value("${EXECUTION_NAME}")
            self.EXECUTION_DESCRIPTION = BuiltIn().get_variable_value("${EXECUTION_DESCRIPTION}")
            self.PRE_RUNNER = 1

            # Connect to db
            self.con = connect_to_mysql_db(self.HOST, self.USER_NAME, self.PASSWORD, self.DATABASE_NAME)
            # create tables if not exist
            create_mysql_tables(self.con)
            # insert values into execution table
            self.id = insert_into_results_mysql_table(self.con, str(self.date_now), self.EXECUTION_NAME)

    def start_test(self, name, attrs):
        self.t_start_time = datetime.datetime.now().time().strftime('%H:%M:%S')

    def end_test(self, name, attrs):
        if self.test_count != 0:
            self.total_tests += 1

        if attrs['status'] == 'PASS':
            self.passed_tests += 1
        else:
            self.failed_tests += 1

        self.t_end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.t_total_time=(datetime.datetime.strptime(self.t_end_time,'%H:%M:%S') - datetime.datetime.strptime(self.t_start_time,'%H:%M:%S'))
        # insert values into test table
        insert_into_test_results_mysql_table(self.con, self.id, str(self.suite_name) + " - " + str(name), str(attrs['status']), str(self.t_total_time), str(attrs['message']))

    def close(self):
        self.end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.total_time=(datetime.datetime.strptime(self.end_time,'%H:%M:%S') - datetime.datetime.strptime(self.start_time,'%H:%M:%S'))
        # insert values into results table
        update_results_mysql_table(self.con, self.id, str(self.total_tests), str(self.passed_tests), str(self.failed_tests), str(self.total_time))

'''

# * # * # * # * Re-usable methods out of class * # * # * # * #

''' 

def get_current_date_time(format,trim):
    t = datetime.datetime.now()
    if t.microsecond % 1000 >= 500:  # check if there will be rounding up
        t = t + datetime.timedelta(milliseconds=1)  # manually round up
    if trim:
        return t.strftime(format)[:-3]
    else:
        return t.strftime(format)

def connect_to_mysql_db(host, user, pwd, db):
    try: 
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db
        )
        return mydb
    except Exception:
        print(Exception)

def create_mysql_tables(con): 
    cursorObj = con.cursor()
    try:
        cursorObj.execute("CREATE TABLE IF NOT EXISTS results(ID int not null auto_increment primary key, DATE text, NAME text, TOTAL text, PASSED text, FAILED text, TIME text)") 
        cursorObj.execute("CREATE TABLE IF NOT EXISTS test_results(ID int, TESTCASE text, STATUS text, TIME text, MESSAGE text)") 
        con.commit()
    except Exception:
        print(Exception)

def insert_into_results_mysql_table(con, date, name):
    cursorObj = con.cursor()
    sql = "INSERT INTO results (ID, DATE, NAME, TOTAL, PASSED, FAILED, TIME) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (0, date, name, "0", "0", "0", "0")
    cursorObj.execute(sql, val)
    con.commit()
    cursorObj.execute("select count(*) from results")
    rows = cursorObj.fetchone()
    return str(rows[0])

def update_results_mysql_table(con, eid, total, passed, failed, duration):
    cursorObj = con.cursor()
    sql = "UPDATE results SET TOTAL=%s, PASSED=%s, FAILED=%s, TIME='%s' WHERE ID=%s;" % (str(total), str(passed), str(failed), str(duration), int(eid))
    cursorObj.execute(sql)
    con.commit()

def insert_into_test_results_mysql_table(con, eid, test, status, duration, msg):
    cursorObj = con.cursor()
    sql = "INSERT INTO test_results (ID, TESTCASE, STATUS, TIME, MESSAGE) VALUES (%s, %s, %s, %s, %s)"
    val = (eid, test, status, duration, msg)
    cursorObj.execute(sql, val)
    # Skip commit to avoid load on db (commit once execution is done as part of close)
    # con.commit()