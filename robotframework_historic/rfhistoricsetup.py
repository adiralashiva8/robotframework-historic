from .dal.adaptors.mysql_adaptor import MySqlDb
import logging

def rfhistoric_setup(opts):

    mysql_server_config = {
        "host": opts.host,
        "username": opts.username,
        "password": opts.password
    }
    # connect to database
    print("INFO: Connecting to dB")
    mydb = MySqlDb(**mysql_server_config)
    mydb.connect()
    # create new user
    obj = mydb.cursor
    print("INFO: Creating superuser with local access")
    try:
        obj.execute("CREATE USER IF NOT EXISTS 'superuser'@'localhost' IDENTIFIED BY 'passw0rd';")
        obj.execute("GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'localhost' WITH GRANT OPTION;")
    except Exception as e:
        print(str(e))
    
    print("INFO: Creating superuser with remote access")
    try:
        obj.execute("CREATE USER 'superuser'@'%' IDENTIFIED BY 'passw0rd';")
        obj.execute("GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'%' WITH GRANT OPTION;")
    except Exception as e:
        print(str(e))
    
    print("INFO: Reloading grant table")
    try:
        obj.execute("FLUSH PRIVILEGES;")
    except Exception as e:
        print(str(e))
    
    print("INFO: Creating robothistoric dB")
    try:
        obj.execute("CREATE DATABASE IF NOT EXISTS robothistoric;")
    except Exception as e:
        print(str(e))

    print("INFO: Creating TB_PROJECT table")
    mydb.use_db("robothistoric")
    try:
        mydb.cursor.execute("CREATE TABLE IF NOT EXISTS TB_PROJECT ( Project_Id INT NOT NULL auto_increment primary key, Project_Name TEXT, Project_Desc TEXT, Project_Image TEXT, Created_Date DATETIME, Last_Updated DATETIME, Total_Executions INT, Recent_Pass_Perc FLOAT, Overall_Pass_Perc FLOAT);")
    except Exception as e:
        print(str(e))

    mydb.commit_close()
