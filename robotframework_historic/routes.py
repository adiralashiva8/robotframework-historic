import pkg_resources
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from robotframework_historic.dal.adaptors.mysql_adaptor import MySqlDb
from robotframework_historic.utils import config
from robotframework_historic.utils.utils import Utils

router = APIRouter()

_mysql = MySqlDb(**config.settings.mysql_config)
_mysql.connect()
cursor = _mysql.cursor

templates = Jinja2Templates(directory=pkg_resources.resource_filename(__name__, 'templates'))

@router.get('/', include_in_schema=False)
def index(request: Request):
    return RedirectResponse(url='/home', status_code=status.HTTP_303_SEE_OTHER)

@router.get('/redirect', include_in_schema=False)
def redirect_url(request: Request):
    return templates.TemplateResponse("redirect.html", {"request": request})


@router.get('/home', include_in_schema=False)
def home(request: Request):
    _mysql.use_db("robothistoric")
    cursor.execute("SELECT * FROM TB_PROJECT;")
    data = cursor.fetchall()
    return templates.TemplateResponse("home.html", {"request": request, "data": data})


@router.get('/updatedb', tags=['ProjectSetup'])
def updatedb_url(request: Request):
    return templates.TemplateResponse("updatedb.html", {"request": request})


@router.get('/{db}/deldbconf', tags=['ProjectSetup'])
def delete_db_conf(db: str, request: Request):
    return templates.TemplateResponse("deldbconf.html", {"request": request, "db_name": db})


@router.get('/{db}/delete', tags=['ProjectSetup'])
def delete_db(db: str):
    cursor.execute("DROP DATABASE %s;" % db)
    # _mysql.use_db("robothistoric")
    cursor.execute("DELETE FROM robothistoric.TB_PROJECT WHERE Project_Name='%s';" % db)
    _mysql.connection.commit()
    return RedirectResponse(url='/home', status_code=status.HTTP_303_SEE_OTHER)


@router.post('/newdb', tags=['ProjectSetup'])
@router.get('/newdb', tags=['ProjectSetup'])
async def add_db(request: Request):
    if request.method == "POST":
        form = await request.form()
        db_name = form['dbname']
        db_desc = form['dbdesc']
        db_image = form['dbimage']

        try:
            # create new database for project
            cursor.execute("Create DATABASE %s;" % db_name)
            # update created database info in robothistoric.TB_PROJECT table
            cursor.execute(
                "INSERT INTO robothistoric.TB_PROJECT ( Project_Id, Project_Name, Project_Desc, Project_Image, Created_Date, Last_Updated, Total_Executions, Recent_Pass_Perc, Overall_Pass_Perc) VALUES (0, '%s', '%s', '%s', NOW(), NOW(), 0, 0, 0);" % (
                    db_name, db_desc, db_image))
            # create tables in created database
            _mysql.use_db(db_name)
            cursor.execute(
                "Create table TB_EXECUTION ( Execution_Id INT NOT NULL auto_increment primary key, Execution_Date DATETIME, Execution_Desc TEXT, Execution_Total INT, Execution_Pass INT, Execution_Fail INT, Execution_Time FLOAT, Execution_STotal INT, Execution_SPass INT, Execution_SFail INT, Execution_Skip INT, Execution_SSkip INT);")
            cursor.execute(
                "Create table TB_SUITE ( Suite_Id INT NOT NULL auto_increment primary key, Execution_Id INT, Suite_Name TEXT, Suite_Status CHAR(4), Suite_Total INT, Suite_Pass INT, Suite_Fail INT, Suite_Time FLOAT, Suite_Skip INT);")
            cursor.execute(
                "Create table TB_TEST ( Test_Id INT NOT NULL auto_increment primary key, Execution_Id INT, Test_Name TEXT, Test_Status CHAR(4), Test_Time FLOAT, Test_Error TEXT, Test_Comment TEXT, Test_Assigned_To TEXT, Test_ETA TEXT, Test_Review_By TEXT, Test_Issue_Type TEXT, Test_Tag TEXT, Test_Updated DATETIME);")
            _mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return RedirectResponse(url='/home', status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse("newdb.html", {"request": request})


@router.get('/{db}/dashboardAll', tags=['Dashboards'])
def dashboard_all(request: Request, db):
    _mysql.use_db(db)
    cursor.execute("SELECT COUNT(Execution_Id) from TB_EXECUTION;")
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Suite_Id) from TB_SUITE;")
    suite_results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Test_Id) from TB_TEST;")
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and suite_results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute(
            "SELECT ROUND(AVG(Execution_Pass),0), ROUND(AVG(Execution_Fail),0), ROUND(AVG(Execution_Time),2), ROUND(AVG(Execution_Skip),0) from TB_EXECUTION;")
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT ROUND((Execution_Pass/Execution_Total)*100, 2) from TB_EXECUTION;")
        exe_perc_data = cursor.fetchall()

        results = []
        results.append(Utils.get_count_by_perc(exe_perc_data, 100, 90))
        results.append(Utils.get_count_by_perc(exe_perc_data, 89, 80))
        results.append(Utils.get_count_by_perc(exe_perc_data, 79, 70))
        results.append(Utils.get_count_by_perc(exe_perc_data, 69, 60))
        results.append(Utils.get_count_by_perc(exe_perc_data, 59, 0))

        return templates.TemplateResponse("dashboard_all.html", {"request": request, "exe_id_avg_data": exe_id_avg_data,
                                                                 "results": results, "results_data": results_data,
                                                                 "db_name": db})

    else:
        return RedirectResponse(url='/redirect', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{db}/dashboardRecent', tags=['Dashboards'])
def dashboardRecent(db: str, request: Request):
    _mysql.use_db(db)

    cursor.execute("SELECT COUNT(Execution_Id) from TB_EXECUTION;")
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Suite_Id) from TB_SUITE;")
    suite_results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Test_Id) from TB_TEST;")
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and suite_results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT Execution_Id, Execution_Total from TB_EXECUTION order by Execution_Id desc LIMIT 2;")
        exe_info = cursor.fetchall()

        if len(exe_info) == 2:
            pass
        else:
            exe_info = (exe_info[0], exe_info[0])

        # handle db columns not exist issue
        try:
            cursor.execute(
                "SELECT Execution_Pass, Execution_Fail, Execution_Total, Execution_Time, Execution_Skip from TB_EXECUTION WHERE Execution_Id=%s;" %
                exe_info[0][0])
            last_exe_data = cursor.fetchall()

            cursor.execute(
                "SELECT Execution_Pass, Execution_Fail, Execution_Total, Execution_Time, Execution_Skip from TB_EXECUTION WHERE Execution_Id=%s;" %
                exe_info[1][0])
            prev_exe_data = cursor.fetchall()

            cursor.execute(
                "SELECT COUNT(*) from TB_TEST WHERE Execution_Id=%s AND Test_Status = 'FAIL' AND Test_Comment IS NULL;" %
                exe_info[0][0])
            req_anal_data = cursor.fetchall()

            cursor.execute("SELECT ROUND(AVG(Suite_Time),2) from TB_SUITE WHERE Execution_Id=%s;" % exe_info[0][0])
            suite_avg_dur_data = cursor.fetchall()

            cursor.execute("SELECT ROUND(AVG(Test_Time),2) from TB_TEST WHERE Execution_Id=%s;" % exe_info[0][0])
            test_avg_dur_data = cursor.fetchall()

            cursor.execute(
                "SELECT b.Suite_Name, a.Suite_Fail, b.Occurence from TB_SUITE a INNER JOIN (Select Suite_Name, Count(Suite_Name) as Occurence From TB_SUITE WHERE Suite_Status = 'FAIL' AND Execution_Id>=%s GROUP BY Suite_Name HAVING COUNT(Suite_Name) > 1) b ON a.Suite_Name = b.Suite_Name WHERE Suite_Status='FAIL' AND Execution_Id=%s ORDER BY b.Occurence DESC, a.Suite_Fail DESC LIMIT 5;" % (
                    exe_info[-1][0], exe_info[0][0]))
            common_failed_suites = cursor.fetchall()

            cursor.execute(
                "SELECT COUNT(*) From (SELECT Test_Name, Execution_Id From TB_TEST WHERE Test_Status='FAIL' AND Execution_Id >= %s GROUP BY Test_Name HAVING COUNT(Test_Name) = 1) AS T WHERE Execution_Id=%s" % (
                    exe_info[1][0], exe_info[0][0]))
            new_failed_tests_count = cursor.fetchall()

            cursor.execute(
                "SELECT COUNT(*) from TB_TEST WHERE Execution_Id=%s AND Test_Issue_Type LIKE '%%Application%%';" %
                exe_info[0][0])
            app_failure_anl_count = cursor.fetchall()

            cursor.execute(
                "SELECT COUNT(*) from TB_TEST WHERE Execution_Id=%s AND Test_Issue_Type LIKE '%%Automation%%';" %
                exe_info[0][0])
            auto_failure_anl_count = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) from TB_TEST WHERE Execution_Id=%s AND Test_Issue_Type LIKE '%%Other%%';" %
                           exe_info[0][0])
            other_failure_anl_count = cursor.fetchall()

            # required analysis percentage
            if last_exe_data[0][1] > 0 and last_exe_data[0][1] != req_anal_data[0][0]:
                req_anal_perc_data = round(((last_exe_data[0][1] - req_anal_data[0][0]) / last_exe_data[0][1]) * 100, 2)
            else:
                req_anal_perc_data = 0

            new_tests_count = exe_info[0][1] - exe_info[1][1]
            passed_test_dif = last_exe_data[0][0] - prev_exe_data[0][0]
            failed_test_dif = prev_exe_data[0][1] - last_exe_data[0][1]
            skipped_test_dif = prev_exe_data[0][4] - last_exe_data[0][4]

            return templates.TemplateResponse('dashboardRecent.html', {"request": request,
                                                                       "last_exe_data": last_exe_data,
                                                                       "exe_info": exe_info,
                                                                       "prev_exe_data": prev_exe_data,
                                                                       "new_failed_tests_count": new_failed_tests_count,
                                                                       "req_anal_data": req_anal_data,
                                                                       "app_failure_anl_count": app_failure_anl_count,
                                                                       "req_anal_perc_data": req_anal_perc_data,
                                                                       "auto_failure_anl_count": auto_failure_anl_count,
                                                                       "new_tests_count": new_tests_count,
                                                                       "other_failure_anl_count": other_failure_anl_count,
                                                                       "passed_test_dif": passed_test_dif,
                                                                       "failed_test_dif": failed_test_dif,
                                                                       "skipped_test_dif": skipped_test_dif,
                                                                       "suite_avg_dur_data": suite_avg_dur_data,
                                                                       "test_avg_dur_data": test_avg_dur_data,
                                                                       "common_failed_suites": common_failed_suites,
                                                                       "db_name": db})
        except Exception as e:
            print(str(e))
            return RedirectResponse(url='/updatedb', status_code=status.HTTP_303_SEE_OTHER)

    else:
        return RedirectResponse(url='/redirect', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{db}/dashboard/{eid}', tags=['Dashboards'])
def eid_dashboard(db, eid, request: Request):
    _mysql.use_db(db)

    cursor.execute("SELECT COUNT(Execution_Id) from TB_EXECUTION;")
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Suite_Id) from TB_SUITE;")
    suite_results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Test_Id) from TB_TEST;")
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and suite_results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute(
            "SELECT Execution_Id, Execution_Total from TB_EXECUTION WHERE Execution_Id <=%s order by Execution_Id desc LIMIT 2;" % eid)
        exe_info = cursor.fetchall()

        if len(exe_info) == 2:
            pass
        else:
            exe_info = (exe_info[0], exe_info[0])

        cursor.execute(
            "SELECT Execution_Pass, Execution_Fail, Execution_Total, Execution_Time, Execution_Skip from TB_EXECUTION WHERE Execution_Id=%s;" %
            exe_info[0][0])
        last_exe_data = cursor.fetchall()

        cursor.execute(
            "SELECT Execution_Pass, Execution_Fail, Execution_Total, Execution_Time, Execution_Skip from TB_EXECUTION WHERE Execution_Id=%s;" %
            exe_info[1][0])
        prev_exe_data = cursor.fetchall()

        cursor.execute(
            "SELECT COUNT(*) from TB_TEST WHERE Execution_Id=%s AND Test_Status = 'FAIL' AND Test_Comment IS NULL;" %
            exe_info[0][0])
        req_anal_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(Suite_Time),2) from TB_SUITE WHERE Execution_Id=%s;" % exe_info[0][0])
        suite_avg_dur_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(Test_Time),2) from TB_TEST WHERE Execution_Id=%s;" % exe_info[0][0])
        test_avg_dur_data = cursor.fetchall()

        cursor.execute(
            "SELECT b.Suite_Name, a.Suite_Fail, b.Occurence from TB_SUITE a INNER JOIN (Select Suite_Name, Count(Suite_Name) as Occurence From TB_SUITE WHERE Suite_Status = 'FAIL' AND Execution_Id IN (%s, %s) GROUP BY Suite_Name HAVING COUNT(Suite_Name) > 1) b ON a.Suite_Name = b.Suite_Name WHERE Suite_Status='FAIL' AND Execution_Id=%s ORDER BY b.Occurence DESC, a.Suite_Fail DESC LIMIT 5;" % (
                exe_info[-1][0], exe_info[0][0], exe_info[0][0]))
        common_failed_suites = cursor.fetchall()

        cursor.execute(
            "SELECT COUNT(*) From (SELECT Test_Name, Execution_Id From TB_TEST WHERE Test_Status='FAIL' AND Execution_Id >= %s GROUP BY Test_Name HAVING COUNT(Test_Name) = 1) AS T WHERE Execution_Id=%s" % (
                exe_info[1][0], exe_info[0][0]))
        new_failed_tests_count = cursor.fetchall()

        cursor.execute(
            "SELECT COUNT(*) from TB_TEST WHERE Execution_Id=%s AND Test_Issue_Type LIKE '%%Application%%';" %
            exe_info[0][0])
        app_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from TB_TEST WHERE Execution_Id=%s AND Test_Issue_Type LIKE '%%Automation%%';" %
                       exe_info[0][0])
        auto_failure_anl_count = cursor.fetchall()

        cursor.execute(
            "SELECT COUNT(*) from TB_TEST WHERE Execution_Id=%s AND Test_Issue_Type LIKE '%%Other%%';" % exe_info[0][0])
        other_failure_anl_count = cursor.fetchall()

        # required analysis percentage
        if last_exe_data[0][1] > 0 and last_exe_data[0][1] != req_anal_data[0][0]:
            req_anal_perc_data = round(((last_exe_data[0][1] - req_anal_data[0][0]) / last_exe_data[0][1]) * 100, 2)
        else:
            req_anal_perc_data = 0

        new_tests_count = exe_info[0][1] - exe_info[1][1]
        passed_test_dif = last_exe_data[0][0] - prev_exe_data[0][0]
        failed_test_dif = prev_exe_data[0][1] - last_exe_data[0][1]
        skipped_test_dif = prev_exe_data[0][4] - last_exe_data[0][4]

        context = {
            "request": request, "last_exe_data": last_exe_data, "exe_info": exe_info, "prev_exe_data": prev_exe_data,
            "new_failed_tests_count": new_failed_tests_count, "req_anal_data": req_anal_data,
            "app_failure_anl_count": app_failure_anl_count, "req_anal_perc_data": req_anal_perc_data,
            "auto_failure_anl_count": auto_failure_anl_count, "new_tests_count": new_tests_count,
            "other_failure_anl_count": other_failure_anl_count, "passed_test_dif": passed_test_dif,
            "failed_test_dif": failed_test_dif, "skipped_test_dif": skipped_test_dif,
            "suite_avg_dur_data": suite_avg_dur_data, "test_avg_dur_data": test_avg_dur_data,
            "common_failed_suites": common_failed_suites, "db_name": db
        }

        return templates.TemplateResponse('dashboardByEid.html', context)

    else:
        return RedirectResponse(url='/redirect', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{db}/dashboardRecentFive', tags=['RecentExecutions'])
def dashboardRecentFive(db: str, request: Request):
    _mysql.use_db(db)
    cursor.execute("SELECT COUNT(Execution_Id) from TB_EXECUTION;")
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Suite_Id) from TB_SUITE;")
    suite_results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Test_Id) from TB_TEST;")
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and suite_results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT Execution_Id, Execution_Total from TB_EXECUTION order by Execution_Id desc LIMIT 5;")
        exe_info = cursor.fetchall()

        cursor.execute(
            "SELECT ROUND(AVG(Execution_Pass),0), ROUND(AVG(Execution_Fail),0), ROUND(AVG(Execution_Time),2), ROUND(AVG(Execution_Skip),0) from TB_EXECUTION WHERE Execution_Id >= %s;" %
            exe_info[-1][0])
        exe_id_avg_data = cursor.fetchall()

        cursor.execute(
            "SELECT Execution_Id, Execution_Pass, Execution_Fail, Execution_Time, Execution_Skip from TB_EXECUTION order by Execution_Id desc LIMIT 5;")
        exe_id_filter_data = cursor.fetchall()

        cursor.execute(
            "SELECT b.Suite_Name, a.Suite_Fail, b.Occurence from TB_SUITE a INNER JOIN (Select Suite_Name, Count(Suite_Name) as Occurence From TB_SUITE WHERE Suite_Status = 'FAIL' AND Execution_Id>=%s GROUP BY Suite_Name HAVING COUNT(Suite_Name) > 1) b ON a.Suite_Name = b.Suite_Name WHERE Suite_Status='FAIL' AND Execution_Id=%s ORDER BY b.Occurence DESC, a.Suite_Fail DESC LIMIT 5;" % (
            exe_info[-1][0], exe_info[0][0]))
        common_failed_suites = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        context = {"request": request, "exe_id_avg_data": exe_id_avg_data, "exe_id_filter_data": exe_id_filter_data,
                   "results_data": results_data, "common_failed_suites": common_failed_suites, "new_tests": new_tests,
                   "db_name": db
                   }

        return templates.TemplateResponse('dashboardRecentFive.html', context)

    else:
        return RedirectResponse(url='/redirect', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{db}/dashboardRecentTen', tags=['RecentExecutions'])
def dashboardRecentTen(db: str, request: Request):
    _mysql.use_db(db)
    cursor.execute("SELECT COUNT(Execution_Id) from TB_EXECUTION;")
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Suite_Id) from TB_SUITE;")
    suite_results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Test_Id) from TB_TEST;")
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and suite_results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT Execution_Id, Execution_Total from TB_EXECUTION order by Execution_Id desc LIMIT 10;")
        exe_info = cursor.fetchall()

        cursor.execute(
            "SELECT ROUND(AVG(Execution_Pass),0), ROUND(AVG(Execution_Fail),0), ROUND(AVG(Execution_Time),2), ROUND(AVG(Execution_Skip),0) from TB_EXECUTION WHERE Execution_Id >= %s;" %
            exe_info[-1][0])
        exe_id_avg_data = cursor.fetchall()

        cursor.execute(
            "SELECT Execution_Id, Execution_Pass, Execution_Fail, Execution_Time, Execution_Skip from TB_EXECUTION order by Execution_Id desc LIMIT 10;")
        exe_id_filter_data = cursor.fetchall()

        cursor.execute(
            "SELECT b.Suite_Name, a.Suite_Fail, b.Occurence from TB_SUITE a INNER JOIN (Select Suite_Name, Count(Suite_Name) as Occurence From TB_SUITE WHERE Suite_Status = 'FAIL' AND Execution_Id>=%s GROUP BY Suite_Name HAVING COUNT(Suite_Name) > 1) b ON a.Suite_Name = b.Suite_Name WHERE Suite_Status='FAIL' AND Execution_Id=%s ORDER BY b.Occurence DESC, a.Suite_Fail DESC LIMIT 5;" % (
            exe_info[-1][0], exe_info[0][0]))
        common_failed_suites = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        context = {"request": request, "exe_id_avg_data": exe_id_avg_data, "exe_id_filter_data": exe_id_filter_data,
                   "results_data": results_data, "common_failed_suites": common_failed_suites, "new_tests": new_tests,
                   "db_name": db
                   }

        return templates.TemplateResponse('dashboardRecentTen.html', context)

    else:
        return RedirectResponse(url='/redirect', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{db}/dashboardRecentThirty', tags=['RecentExecutions'])
def dashboardRecentThirty(db: str, request: Request):
    _mysql.use_db(db)
    cursor.execute("SELECT COUNT(Execution_Id) from TB_EXECUTION;")
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Suite_Id) from TB_SUITE;")
    suite_results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(Test_Id) from TB_TEST;")
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and suite_results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT Execution_Id, Execution_Total from TB_EXECUTION order by Execution_Id desc LIMIT 30;")
        exe_info = cursor.fetchall()

        cursor.execute(
            "SELECT ROUND(AVG(Execution_Pass),0), ROUND(AVG(Execution_Fail),0), ROUND(AVG(Execution_Time),2), ROUND(AVG(Execution_Skip),0) from TB_EXECUTION WHERE Execution_Id >= %s;" %
            exe_info[-1][0])
        exe_id_avg_data = cursor.fetchall()

        cursor.execute(
            "SELECT Execution_Id, Execution_Pass, Execution_Fail, Execution_Time, Execution_Skip from TB_EXECUTION order by Execution_Id desc LIMIT 30;")
        exe_id_filter_data = cursor.fetchall()

        cursor.execute(
            "SELECT b.Suite_Name, a.Suite_Fail, b.Occurence from TB_SUITE a INNER JOIN (Select Suite_Name, Count(Suite_Name) as Occurence From TB_SUITE WHERE Suite_Status = 'FAIL' AND Execution_Id>=%s GROUP BY Suite_Name HAVING COUNT(Suite_Name) > 1) b ON a.Suite_Name = b.Suite_Name WHERE Suite_Status='FAIL' AND Execution_Id=%s ORDER BY b.Occurence DESC, a.Suite_Fail DESC LIMIT 5;" % (
            exe_info[-1][0], exe_info[0][0]))
        common_failed_suites = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        context = {"request": request, "exe_id_avg_data": exe_id_avg_data, "exe_id_filter_data": exe_id_filter_data,
                   "results_data": results_data, "common_failed_suites": common_failed_suites, "new_tests": new_tests,
                   "db_name": db
                   }

        return templates.TemplateResponse('dashboardRecentThirty.html', context)
    else:
        return RedirectResponse(url='/redirect', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/{db}/ehistoric', tags=['HistoricExecutions'])
def ehistoric(db: str, request: Request):
    _mysql.use_db(db)
    cursor.execute("SELECT * from TB_EXECUTION order by Execution_Id desc LIMIT 500;")
    data = cursor.fetchall()
    return templates.TemplateResponse('ehistoric.html', {"request": request, "data": data, "db_name": db})


@router.get('/{db}/deleconf/{eid}', tags=['ProjectSetup'])
def delete_eid_conf(db: str, eid: int, request: Request):
    return templates.TemplateResponse('deleconf.html', {"request": request, "db_name": db, "eid": eid})


@router.get('/{db}/edelete/{eid}', tags=['ProjectSetup'])
def delete_eid(db, eid):
    _mysql.use_db(db)
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
            recent_pass_perf = float("{0:.2f}".format((data[0][0] / data[0][1] * 100)))
        else:
            recent_pass_perf = 0
    except:
        recent_pass_perf = 0

    # update robothistoric project
    cursor.execute(
        "UPDATE robothistoric.TB_PROJECT SET Total_Executions=%s, Last_Updated=now(), Recent_Pass_Perc=%s WHERE Project_Name='%s';" % (
            int(exe_data[0][0]), recent_pass_perf, db))
    # commit changes
    _mysql.connection.commit()
    return RedirectResponse(url=f"/{db}/ehistoric")


@router.get('/{db}/tmetrics', tags=['Metrics'])
@router.post('/{db}/tmetrics', tags=['Metrics'])
async def tmetrics(db: str, request: Request):
    _mysql.use_db(db)
    if request.method == "POST":
        form = await request.form()
        issue_type = form['issue']
        review_by = form['reviewby']
        assign_to = form['assignto']
        eta = form['eta']
        comment = form['comment']
        rowid = form['rowid']
        cursor.execute(
            'Update TB_TEST SET Test_Comment=\'%s\', Test_Assigned_To=\'%s\', Test_ETA=\'%s\', Test_Review_By=\'%s\', Test_Issue_Type=\'%s\', Test_Updated=now() WHERE Test_Id=%s;' % (
                str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        _mysql.connection.commit()

    # Get last row execution ID
    cursor.execute("SELECT Execution_Id from TB_EXECUTION order by Execution_Id desc LIMIT 1;")
    data = cursor.fetchone()
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from TB_TEST WHERE Execution_Id=%s;" % data)
    data = cursor.fetchall()
    return templates.TemplateResponse('tmetrics.html', {"request": request, "data": data, "db_name": db})


@router.get('/{db}/metrics/{eid}', tags=['Metrics'])
def metrics(db: str, eid, request: Request):
    _mysql.use_db(db)
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
    return templates.TemplateResponse('metrics.html', {"request": request, "suite_data": suite_data,
                                                       "test_data": test_data, "project_image": project_image[0][0],
                                                       "exe_data": exe_data})


@router.get('/{db}/tmetrics/{eid}', tags=['Metrics'])
@router.post('/{db}/tmetrics/{eid}', tags=['Metrics'])
async def eid_tmetrics(db: str, eid, request: Request):
    _mysql.use_db(db)
    if request.method == "POST":
        form = await request.form()
        issue_type = form['issue']
        review_by = form['reviewby']
        assign_to = form['assignto']
        eta = form['eta']
        comment = form['comment']
        rowid = form['rowid']
        cursor.execute(
            'Update TB_TEST SET Test_Comment=\'%s\', Test_Assigned_To=\'%s\', Test_ETA=\'%s\', Test_Review_By=\'%s\', Test_Issue_Type=\'%s\', Test_Updated=now() WHERE Test_Id=%s;' % (
                str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        _mysql.connection.commit()

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from TB_TEST WHERE Execution_Id=%s;" % eid)
    data = cursor.fetchall()
    return templates.TemplateResponse('eidtmetrics.html', {"request": request, "data": data, "db_name": db})


@router.get('/{db}/failures/{eid}', tags=['TestResults'])
@router.post('/{db}/failures/{eid}', tags=['TestResults'])
async def eid_failures(db, eid, request: Request):
    _mysql.use_db(db)
    if request.method == "POST":
        form = await request.form()
        issue_type = form['issue']
        review_by = form['reviewby']
        assign_to = form['assignto']
        eta = form['eta']
        comment = form['comment']
        rowid = form['rowid']
        cursor.execute(
            'Update TB_TEST SET Test_Comment=\'%s\', Test_Assigned_To=\'%s\', Test_ETA=\'%s\', Test_Review_By=\'%s\', Test_Issue_Type=\'%s\', Test_Updated=now() WHERE Test_Id=%s;' % (
                str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        _mysql.connection.commit()

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from TB_TEST WHERE Execution_Id=%s and Test_Status='FAIL';" % eid)
    data = cursor.fetchall()
    return templates.TemplateResponse('failures.html', {"request": request, "data": data, "db_name": db})


@router.get('/{db}/failures', tags=['TestResults'])
@router.post('/{db}/failures', tags=['TestResults'])
async def recent_failures(db: str, request: Request):
    _mysql.use_db(db)
    if request.method == "POST":
        form = await request.form()
        issue_type = form['issue']
        review_by = form['reviewby']
        assign_to = form['assignto']
        eta = form['eta']
        comment = form['comment']
        rowid = form['rowid']
        cursor.execute(
            'Update TB_TEST SET Test_Comment=\'%s\', Test_Assigned_To=\'%s\', Test_ETA=\'%s\', Test_Review_By=\'%s\', Test_Issue_Type=\'%s\', Test_Updated=now() WHERE Test_Id=%s;' % (
                str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        _mysql.connection.commit()

    # Get last row execution ID
    cursor.execute("SELECT Execution_Id from TB_EXECUTION order by Execution_Id desc LIMIT 1;")
    data = cursor.fetchone()
    cursor.execute("SELECT * from TB_TEST WHERE Execution_Id=%s and Test_Status='FAIL';" % data)
    data = cursor.fetchall()
    return templates.TemplateResponse('failures.html', {"request": request, "data": data, "db_name": db})


@router.get('/{db}/ttags/{eid}', tags=['TestTags'])
@router.post('/{db}/ttags/{eid}', tags=['TestTags'])
def eid_ttags(db, eid, request: Request):
    _mysql.use_db(db)
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT Execution_Id, Test_Name, Test_Status, Test_Tag from TB_TEST WHERE Execution_Id=%s" % eid)
    data = cursor.fetchall()
    return templates.TemplateResponse('ttags.html', {"request": request, "data": data, "db_name": db})


@router.get('/{db}/search')
@router.post('/{db}/search')
async def search(db: str, request: Request):
    if request.method == "POST":
        form = await request.form()
        search = form['search']
        _mysql.use_db(db)
        try:
            if search:
                cursor.execute(
                    "SELECT * from TB_TEST WHERE Test_Name LIKE '%{name}%' OR Test_Status LIKE '%{name}%' OR Execution_Id LIKE '%{name}%' ORDER BY Execution_Id DESC LIMIT 500;".format(
                        name=search))
                data = cursor.fetchall()
                return templates.TemplateResponse('search.html', {"request": request, "data": data, "db_name": db,
                                                                  "error_message": ""})
            else:
                return templates.TemplateResponse('search.html', {"request": request, "db_name": db,
                                                                  "error_message": "Search text should not be empty!"})
        except Exception as e:
            print(str(e))
            return templates.TemplateResponse('search.html', {"request": request, "db_name": db,
                                                              "error_message": "Could not perform search. Avoid single quote in search or use escaping character"
                                                              })
    else:
        return templates.TemplateResponse('search.html', {"request": request, "db_name": db, "error_message": ""})


@router.get('/{db}/flaky', tags=['TestResults'])
def flaky(db: str, request: Request):
    _mysql.use_db(db)
    cursor.execute(
        "SELECT Execution_Id from ( SELECT Execution_Id from TB_EXECUTION ORDER BY Execution_Id DESC LIMIT 5 ) as tmp ORDER BY Execution_Id ASC LIMIT 1;")
    last_five = cursor.fetchall()
    cursor.execute("SELECT Execution_Id from TB_EXECUTION ORDER BY Execution_Id DESC LIMIT 5;")
    last_five_ids = cursor.fetchall()
    sql_query = "SELECT Test_Name, Execution_Id, Test_Status from TB_TEST WHERE Execution_Id >= %s ORDER BY Execution_Id DESC;" % (
        str(last_five[0][0]))
    cursor.execute(sql_query)
    data = cursor.fetchall()
    # print("==== Before Sorted Data ===")
    # print(data)
    sorted_data = Utils.sort_tests(data)
    # print("==== After Sorted Data ===")
    # print(sorted_data)
    return templates.TemplateResponse('flaky.html', {"request": request, "db_name": db, "data": sorted_data,
                                                     "builds": last_five_ids})


@router.get('/{db}/compare', tags=['TestAnalysis'])
@router.post('/{db}/compare')
async def compare(db: str, request: Request):
    if request.method == "POST":
        form = await request.form()
        eid_one = form['eid_one']
        eid_two = form['eid_two']
        cursor = _mysql.connection.cursor()
        _mysql.use_db(db)
        # fetch first eid tets results
        cursor.execute(
            "SELECT Test_Name, Execution_Id, Test_Status, Test_Time, Test_Error from TB_TEST WHERE Execution_Id=%s;" % eid_one)
        first_data = cursor.fetchall()
        # fetch second eid test results
        cursor.execute(
            "SELECT Test_Name, Execution_Id, Test_Status, Test_Time, Test_Error from TB_TEST WHERE Execution_Id=%s;" % eid_two)
        second_data = cursor.fetchall()
        if first_data and second_data:
            # combine both tuples
            data = first_data + second_data
            sorted_data = Utils.sort_tests(data)
            return templates.TemplateResponse('compare.html', {"request": request, "data": sorted_data, "db_name": db,
                                                               "fb": first_data, "sb": second_data,
                                                               "eid_one": eid_one, "eid_two": eid_two,
                                                               "error_message": ""})
        else:
            return templates.TemplateResponse('compare.html', {"request": request, "db_name": db,
                                                               "error_message": "EID not found, try with existing EID"})
    else:
        return templates.TemplateResponse('compare.html', {"request": request, "db_name": db, "error_message": ""})


@router.get('/{db}/query', tags=['Query'])
@router.post('/{db}/query', tags=['Query'])
async def query(db: str, request: Request):
    if request.method == "POST":
        form = await request.form()
        query = form['query']
        _mysql.use_db(db)
        try:
            cursor.execute("{name}".format(name=query))
            data = cursor.fetchall()
            return templates.TemplateResponse('query.html', {"request": request, "data": data, "db_name": db,
                                                             "error_message": ""})

        except Exception as e:
            print(str(e))
            return templates.TemplateResponse('query.html',
                                              {"request": request, "db_name": db, "error_message": str(e)})

    else:
        return templates.TemplateResponse('query.html', {"request": request, "db_name": db, "error_message": ""})


@router.get('/{db}/comment', tags=['Comment'])
@router.post('/{db}/comment', tags=['Comment'])
async def comment(db: str, request: Request):
    _mysql.use_db(db)
    cursor.execute("SELECT Execution_Id from TB_EXECUTION order by Execution_Id desc LIMIT 1;")
    recent_eid = cursor.fetchone()

    if request.method == "POST":
        form = await request.form()
        error = form['error']
        eid = form['eid']
        issue_type = form['issue']
        review_by = form['reviewby']
        assign_to = form['assignto']
        eta = form['eta']
        comment = form['comment']

        try:
            cursor.execute(
                'Update TB_TEST SET Test_Comment=\'{}\', Test_Assigned_To=\'{}\', Test_ETA=\'{}\', Test_Review_By=\'{}\', Test_Issue_Type=\'{}\', Test_Updated=now() WHERE Execution_Id={} AND Test_Error LIKE \'%{}%\''.format(
                    str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(eid), str(error)))
            _mysql.connection.commit()
            return templates.TemplateResponse('comment.html', {"request": request, "recent_eid": recent_eid,
                                                               "error_message": ""})
        except Exception as e:
            print(str(e))
            return templates.TemplateResponse('comment.html', {"request": request, "recent_eid": recent_eid,
                                                               "error_message": str(e)})
    else:
        return templates.TemplateResponse('comment.html',
                                          {"request": request, "recent_eid": recent_eid, "error_message": ""})
