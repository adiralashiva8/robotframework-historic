# robotframework-historic
Robotframework report to hold historic results (Flask + MySQL + Robotframework + Tomcat)

---

# About

[Robotframework-historic]() is a custom report to hold historic results of robotframework execution by simply storing execution details in database and generate html reports from database.

- Get execution details by [parsing]() output.xml
- Store execution results in local hosted [MYSQL]() database
- Generate html report using [Flask]()
- [Tomcat]() to act as webserver

# Requirements

 - Python 3.7 or above
 - MySQL
 - Flask
 - flask-mysqldb


# Installation

 - Download and Install python - [Installation Guide]()
 - Download and Install MySQL - [Installation Guide](https://www.softwaretestingclass.com/guide-to-install-mysql-database-and-workbench/)
- Install Flask `pip install flask`
- Install flas-mysqldb `pip install flask-mysqldb`