# robotframework-historic
Robotframework report to hold historic results (Flask + MySQL + Robotframework)

---

# About

[Robotframework-historic]() is a custom report to hold historic results of robotframework execution by simply storing execution details in database and generating html reports from database with charts / statistics.

- Get execution details by [parsing]() output.xml or using listener
- Store execution results in local hosted [MYSQL]() database
- Generate html report using [Flask]()

# Requirements

 - Python 3.7 or above
 - MySQL DB

# Installation

 - Download and Install MySQL Server - [Installation Guide](https://www.softwaretestingclass.com/guide-to-install-mysql-database-and-workbench/) - One time activity
- Install robotframework_historic - One time activity

# Default SQL User:
 - User Name: superuser
 - Password: passw0rd

# Default SQL Info:

 - Port: 3306
 - Host: localhost / mysql hosted machine ip

# Check sql connection
  `mysql> -u<superuser> -h <ip> -P 3306 -p<passwOrd>`

# Create your own user (one time activity)

 - Create user query
   `CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';`

 - Grant permissions
   `GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';`