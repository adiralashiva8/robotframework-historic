import os
import mysql.connector
import logging
from robot.api import ExecutionResult, ResultVisitor
import datetime
from datetime import timedelta

def rfhistoric_parser(opts):

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

    test_stats = SuiteStats()
    result.visit(test_stats)

    try:
        test_stats_obj = test_stats.all
    except:
        test_stats_obj = test_stats
    stotal = test_stats_obj.total_suite
    spass = test_stats_obj.passed_suite
    sfail = test_stats_obj.failed_suite
    try:
        sskip = test_stats_obj.skipped_suite
    except:
        sskip = 0

    stats = result.statistics
    try:
        stats_obj = stats.total.all
    except:
        stats_obj = stats.total
    total = stats_obj.total
    passed = stats_obj.passed
    failed = stats_obj.failed
    try:
        skipped = stats_obj.skipped
    except:
        skipped = 0

    elapsedtime = datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=result.suite.elapsedtime)
    elapsedtime = get_time_in_min(elapsedtime.strftime("%X"))
    elapsedtime = float("{0:.2f}".format(elapsedtime))

    # insert test results info into db
    result_id = insert_into_execution_table(mydb, rootdb, opts.executionname, total, passed, failed, elapsedtime, stotal, spass, sfail, skipped, sskip, opts.projectname)

    print("INFO: Capturing suite results")
    result.visit(SuiteResults(mydb, result_id, opts.fullsuitename))
    print("INFO: Capturing test results")
    result.visit(TestMetrics(mydb, result_id, opts.fullsuitename))

    print("INFO: Writing execution results")
    commit_and_close_db(mydb)

# other useful methods
class SuiteStats(ResultVisitor):
    total_suite = 0
    passed_suite = 0
    failed_suite = 0
    skipped_suite = 0

    def start_suite(self, suite):
        suite_test_list = suite.tests
        if not suite_test_list:
            pass
        else:
            self.total_suite += 1

            if suite.status == "PASS":
                self.passed_suite += 1
            elif suite.status == "FAIL":
                self.failed_suite += 1
            else:
                self.skipped_suite += 1

class SuiteResults(ResultVisitor):

    def __init__(self, db, id, full_suite_name):
        self.db = db
        self.id = id
        self.full_suite_name = full_suite_name

    def start_suite(self,suite):

        suite_test_list = suite.tests
        if not suite_test_list:
            pass
        else:
            if self.full_suite_name == "True":
                suite_name = suite.longname
            else:
                suite_name = suite
   
            try:
                stats = suite.statistics.all
            except:
                stats = suite.statistics
            time = float("{0:.2f}".format(suite.elapsedtime / float(60000)))
            # TODO: Update skipped when functionality implemented
            try:
                suite_skipped = stats.skipped
            except:
                suite_skipped = 0
            insert_into_suite_table(self.db, self.id, str(suite_name), str(suite.status), int(stats.total), int(stats.passed), int(stats.failed), float(time), int(suite_skipped))

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
        insert_into_test_table(self.db, self.id, str(name), str(test.status), time, error, str(test.tags))

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

def insert_into_execution_table(con, ocon, name, total, passed, failed, ctime, stotal, spass, sfail, skipped, sskipped, projectname):
    cursorObj = con.cursor()
    rootCursorObj = ocon.cursor()
    sql = "INSERT INTO TB_EXECUTION (Execution_Id, Execution_Date, Execution_Desc, Execution_Total, Execution_Pass, Execution_Fail, Execution_Time, Execution_STotal, Execution_SPass, Execution_SFail, Execution_Skip, Execution_SSkip) VALUES (%s, now(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val = (0, name, total, passed, failed, ctime, stotal, spass, sfail, skipped, sskipped)
    cursorObj.execute(sql, val)
    con.commit()
    cursorObj.execute("SELECT Execution_Id, Execution_Pass, Execution_Total FROM TB_EXECUTION ORDER BY Execution_Id DESC LIMIT 1;")
    rows = cursorObj.fetchone()
    cursorObj.execute("SELECT COUNT(*) FROM TB_EXECUTION;")
    execution_rows = cursorObj.fetchone()
    # update robothistoric.TB_PROJECT table
    rootCursorObj.execute("UPDATE TB_PROJECT SET Last_Updated = now(), Total_Executions = %s, Recent_Pass_Perc =%s WHERE Project_Name='%s';" % (execution_rows[0], float("{0:.2f}".format((rows[1]/rows[2]*100))), projectname))
    ocon.commit()
    return str(rows[0])

def insert_into_suite_table(con, eid, name, status, total, passed, failed, duration, skipped):
    cursorObj = con.cursor()
    sql = "INSERT INTO TB_SUITE (Suite_Id, Execution_Id, Suite_Name, Suite_Status, Suite_Total, Suite_Pass, Suite_Fail, Suite_Time, Suite_Skip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (0, eid, name, status, total, passed, failed, duration, skipped)
    cursorObj.execute(sql, val)
    # Skip commit to avoid load on db (commit once execution is done as part of close)
    # con.commit()

def insert_into_test_table(con, eid, test, status, duration, msg, tags):
    cursorObj = con.cursor()
    sql = "INSERT INTO TB_TEST (Test_Id, Execution_Id, Test_Name, Test_Status, Test_Time, Test_Error, Test_Tag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (0, eid, test, status, duration, msg, tags)
    cursorObj.execute(sql, val)
    # Skip commit to avoid load on db (commit once execution is done as part of close)
    # con.commit()

def commit_and_close_db(db):
    # cursorObj = db.cursor()
    db.commit()
    # cursorObj.close()
    # db.close()