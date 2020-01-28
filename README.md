# robotframework-historic

[Robotframework-historic]() is a free, custom html report which provides historical robotframework execution results by storing execution results info in MYSQL database and generate's html reports (charts / statistics) from database using Flask.

> MYSQL + Flask + Robotframework

![PyPI version](https://badge.fury.io/py/robotframework-historic.svg)
[![Downloads](https://pepy.tech/badge/robotframework-historic)](https://pepy.tech/project/robotframework-historic)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)

---

## Robotframework Historic Overview

### Image here>

---

## Features

- Support Historic Results
- Visualization of execution status like
  - Last 10 execution trends
  - Last 10 execution performance
  - Average pass % of recent 10 executions
  - Average pass % of all executions
  - Average execution time of recent 10 executions
  - Average execution time of all executions
- Search Historical test records by name / status / execution id
- Local hosted (meets privacy concerns)
- Supports multiple projects
- Export results (Excel, CSV, Print, Copy)

---

## Why Robotframework-Historic

- It is free
- Made by QA
- Can customize as per requirements
- No code changes required

---

## How it Works:

- Get execution details by [parsing]() output.xml or using [listener]()
- Store execution results in local / remote hosted [MYSQL]() database
- Generate html report using [Flask]()

<img src="https://i.ibb.co/PzVNGfN/robotframework-historic-overview.png" alt="robotframework-historic-overview" border="0.5" style="border-radius: 15%;">

---

## Requirements

 - Python 3.7 or above
 - MySQL DB

---

## Installation

 - __Step 1:__ Install `robotframework-historic`
    ```
    pip install robotframework-historic
    ```

 - __Step 2:__ Download and Install MySQL Server - [setup mysql guide]()

 - __Step 3:__ Create *rfhistoric* _default user_ with permissions - [create sql user guide]()

 - __Step 4:__ Install `robotframework-historic-parser`
    ```
    pip install robotframework-historic-parser
    ```

 - __Step 5:__ Install `robotframework-historic-listener`
    ```
    pip install robotframework-historic-listener
    ```
 
 > _Note:_ Above all actions are one time activities

---

## How to use in project


---

## Default MySQL User:
 - User Name: superuser
 - Password: passw0rd

## Default SQL Info:

 - Port: 3306
 - Host: localhost / mysql hosted machine ip

## Check sql connection
  `mysql> -u<superuser> -h <ip> -P 3306 -p<passwOrd>`

## Create rfhistoric user (one time activity)

 > Creating user and assigning permission for local and remote access

 ```
   # create local user
  CREATE USER 'superuser'@'localhost' IDENTIFIED BY 'passw0rd';

  # grant local access permission
  GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'localhost' WITH GRANT OPTION;

  # create remote user
  CREATE USER 'superuser'@'%' IDENTIFIED BY 'passw0rd';

  # grant remote access permission
  GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'%' WITH GRANT OPTION;

  # to reload grant table
  FLUSH PRIVILEGES;
 ```

---

:star: repo if you like it

> Inspired from [ZenQ - ARES Dahsboard](http://www.testastra.com/ares/)

---

Thanks for using `robotframework-historic`!

 - What’s your opinion on this report?
 - What’s the feature I should add?

If you have any questions / suggestions / comments on the report, please feel free to reach me at

 - Email: <a href="mailto:adiralashiva8@gmail.com?Subject=Robotframework%20historic" target="_blank">`adiralashiva8@gmail.com`</a> 
 - Slack: <a href="https://robotframework.slack.com/messages/robotframeworkhistoric" target="_blank">`robotframeworkhistoric`</a>
 - LinkedIn: <a href="https://www.linkedin.com/in/shivaprasadadirala/" target="_blank">`shivaprasadadirala`</a>
 - Twitter: <a href="https://twitter.com/ShivaAdirala" target="_blank">`@ShivaAdirala`</a>