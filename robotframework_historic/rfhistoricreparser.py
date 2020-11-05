import os
import mysql.connector
import logging
from robot.api import ExecutionResult, ResultVisitor
import datetime
from datetime import timedelta

def rfhistoric_reparser(opts):

    if opts.ignoreresult == "True":
        print("Ignoring execution results...")
        return

    path = os.path.abspath(os.path.expanduser(opts.path))

    # output.xml files
    output_names = []
    # support "*.xml" of output files
    if ( opts.output == "*.xml" ):
        for item in os.listdir(path):
            if os.path.isfile(item) and item.endswith('.xml'):
                output_names.append(item)
    else:
        for curr_name in opts.output.split(","):
            curr_path = os.path.join(path, curr_name)
            output_names.append(curr_path)

    required_files = list(output_names)
    missing_files = [filename for filename in required_files if not os.path.exists(filename)]
    if missing_files:
        # We have files missing.
        exit("output.xml file is missing: {}".format(", ".join(missing_files)))

    # Read output.xml file
    result = ExecutionResult(*output_names)
    result.configure(stat_config={'suite_stat_level': 2,
                                  'tag_stat_combine': 'tagANDanother'})

    print("Capturing execution results, This may take few minutes...")

    # connect to database
    mydb = connect_to_mysql_db(opts.host, opts.username, opts.password, opts.projectname)
    rootdb = connect_to_mysql_db(opts.host, opts.username, opts.password, 'robothistoric')

    # get latest execution id
    if opts.executionid == "latest":
        result_id = get_latest_execution_id(mydb)
    else:
        result_id = opts.executionid

    print("INFO: Updating test results")
    result.visit(TestMetrics(mydb, result_id, opts.fullsuitename))
    print("INFO: Updating execution table")
    update_execution_table(mydb, rootdb, opts.executionname, opts.projectname, result_id)
    print("INFO: Updating execution results")
    commit_and_close_db(mydb)

class TestMetrics(ResultVisitor):

    def __init__(self, db, id, full_suite_name):
        self.db = db
        self.id = id
        self.full_suite_name = full_suite_name

    def visit_test(self, test):
        if self.full_suite_name == "True":
            full_suite_name = test.longname.split("." + test.name)
            name = str(full_suite_name[0]) + " - " + str(test)
        else:
            name = str(test.parent) + " - " + str(test)

        time = float("{0:.2f}".format(test.elapsedtime / float(60000)))
        error = str(test.message)
        update_test_table(self.db, self.id, str(name), str(test.status), time, error, str(test.tags))

def get_time_in_min(time_str):
    h, m, s = time_str.split(':')
    ctime = int(h) * 3600 + int(m) * 60 + int(s)
    crtime = float("{0:.2f}".format(ctime/60))
    return crtime

def connect_to_mysql_db(host, user, pwd, db):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db
        )
        return mydb
    except Exception as e:
        print(e)
    
def get_latest_execution_id(con):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT Execution_Id FROM TB_EXECUTION ORDER BY Execution_Id DESC LIMIT 1;")
    rows = cursorObj.fetchone()
    return rows[0]

def update_execution_table(con, ocon, name, projectname, eid):
    cursorObj = con.cursor()
    rootCursorObj = ocon.cursor()
    # get pass, fail, skip test cases count by eid
    cursorObj.execute("SELECT COUNT(*) FROM TB_TEST WHERE Execution_Id=%s AND Test_Status='PASS';" % (eid))
    execution_rows = cursorObj.fetchone()
    tests_passed = execution_rows[0]

    cursorObj.execute("SELECT COUNT(*) FROM TB_TEST WHERE Execution_Id=%s AND Test_Status='FAIL';" % (eid))
    execution_rows = cursorObj.fetchone()
    tests_failed = execution_rows[0]

    cursorObj.execute("SELECT COUNT(*) FROM TB_TEST WHERE Execution_Id=%s AND Test_Status='SKIP';" % (eid))
    execution_rows = cursorObj.fetchone()
    tests_skipped = execution_rows[0]

    tests_total = tests_passed + tests_failed + tests_skipped

    sql = "UPDATE TB_EXECUTION SET Execution_Total=%s, Execution_Pass=%s, Execution_Fail=%s, Execution_Skip=%s WHERE Execution_Id=%s;" % (tests_total, tests_passed, tests_failed, tests_skipped, eid)
    cursorObj.execute(sql)
    con.commit()
    cursorObj.execute("SELECT Execution_Id, Execution_Pass, Execution_Total FROM TB_EXECUTION ORDER BY Execution_Id DESC LIMIT 1;")
    rows = cursorObj.fetchone()
    cursorObj.execute("SELECT COUNT(*) FROM TB_EXECUTION;")
    execution_rows = cursorObj.fetchone()
    # update robothistoric.TB_PROJECT table
    rootCursorObj.execute("UPDATE TB_PROJECT SET Last_Updated = now(), Total_Executions = %s, Recent_Pass_Perc =%s WHERE Project_Name='%s';" % (execution_rows[0], float("{0:.2f}".format((rows[1]/rows[2]*100))), projectname))
    ocon.commit()
    return str(rows[0])

def update_test_table(con, eid, test, status, duration, msg, tags):
    cursorObj = con.cursor()
    sql = "UPDATE TB_TEST SET Test_Status = %s, Test_Time = %s, Test_Error = %s, Test_Tag =%s WHERE Test_Name='%s' AND Execution_Id=%s) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (status, duration, msg, tags, test, eid)
    cursorObj.execute(sql, val)
    # Skip commit to avoid load on db (commit once execution is done as part of close)
    # con.commit()

def commit_and_close_db(db):
    # cursorObj = db.cursor()
    db.commit()
    # cursorObj.close()
    # db.close()