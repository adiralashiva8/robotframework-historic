from .dal.adaptors.mysql_adaptor import MySqlDb
import logging


def rfhistoric_update(opts):
    mysql_server_config = {
        "host": opts.host,
        "username": opts.username,
        "password": opts.password,
        "database": "robothistoric"
    }

    rfdb = MySqlDb(**mysql_server_config)
    rfdb.connect()
    # get list of databases
    rfobj = rfdb.cursor
    rfobj.execute("SELECT Project_Name FROM TB_PROJECT;")
    results_data = rfobj.fetchall()

    for item in results_data:
        rfdb.use_db(str(item[0]))
        try:
            print("INFO: Updating TB_EXECUTION table of DB " + str(item[0]))
            execut_query(rfobj, "ALTER TABLE TB_EXECUTION ADD COLUMN Execution_Skip INT NOT NULL DEFAULT 0 ;")
            execut_query(rfobj, "ALTER TABLE TB_EXECUTION ADD COLUMN Execution_SSkip INT NOT NULL DEFAULT 0;")
        except Exception as e:
            print(str(e))

        try:
            print("INFO: Updating TB_SUITE table of DB " + str(item[0]))
            execut_query(rfobj, "ALTER TABLE TB_SUITE ADD COLUMN Suite_Skip INT NOT NULL DEFAULT 0;")
        except Exception as e:
            print(str(e))

        try:
            print("INFO: Updating TB_TEST table of DB " + str(item[0]))
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Assigned_To TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_ETA TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Review_By TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Issue_Type TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Tag TEXT;")
            execut_query(rfobj, "ALTER TABLE TB_TEST ADD COLUMN Test_Updated DATETIME;")
        except Exception as e:
            print(str(e))

    rfdb.commit_close()


def execut_query(rfobj, query):
    try:
        rfobj.execute(query)
    except Exception as e:
        print(str(e))
