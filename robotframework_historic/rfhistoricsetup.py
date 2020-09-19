import mysql.connector
import logging

def rfhistoric_setup(opts):

    # connect to database
    print("INFO: Connecting to dB")
    mydb = connect_to_mysql(opts.host, opts.username, opts.password)

    # create new user
    obj = mydb.cursor()

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
    rfdb = connect_to_mysql_db(opts.host, opts.username, opts.password, "robothistoric")
    try:
        rfdb.execute("CREATE TABLE IF NOT EXISTS TB_PROJECT ( Project_Id INT NOT NULL auto_increment primary key, Project_Name TEXT, Project_Desc TEXT, Project_Image TEXT, Created_Date DATETIME, Last_Updated DATETIME, Total_Executions INT, Recent_Pass_Perc FLOAT, Overall_Pass_Perc FLOAT);")
        rfdb.commit
    except Exception as e:
        print(str(e))

    commit_and_close_db(mydb)

def connect_to_mysql(host, user, pwd):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd
        )
        return mydb
    except Exception as e:
        print(e)

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

def commit_and_close_db(db):
    db.commit()
    db.close()