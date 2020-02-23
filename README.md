# robotframework-historic

Robotframework-historic is a free, custom html report which provides historical robotframework execution results by storing execution results info in MySQL database and generate's html reports (charts / statistics) from database using Flask.

> MYSQL + Flask + Robotframework

![PyPI version](https://badge.fury.io/py/robotframework-historic.svg)
[![Downloads](https://pepy.tech/badge/robotframework-historic)](https://pepy.tech/project/robotframework-historic)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)
[![HitCount](http://hits.dwyl.io/adiralashiva8/robotframework-historic.svg)](http://hits.dwyl.io/adiralashiva8/robotframework-historic)

---

## Robotframework Historic Overview

 > <img src="https://i.ibb.co/Rc37hP7/Webp-net-gifmaker-1.gif" alt="Overview">

---

## Features

- Support Historic Results
- Visualization of execution status like
  - Last 10 execution, performance trends
  - Average pass tests of recent 10, overvall executions
  - Average execution time of recent 10, overall executions
- Search Historical test records by name / status / execution id
- Local hosted (meets privacy concerns)
- Export results (Excel, CSV, Print, Copy)

---

## Why Robotframework-Historic

- It is free
- Made by QA
- Can customize as per requirements
- No code changes required

---

## How it Works:

- Get execution details by __parsing__ output.xml or using __listener__
- Store execution results in local / remote hosted __MySQL__ database
- Generate html report using __Flask__

  > <img src="https://i.ibb.co/PzVNGfN/robotframework-historic-overview.png" alt="robotframework-historic-overview">

---

## Requirements

 - Python 3.7 or above
 - MySQL DB

---

## Installation

 - __Step 1:__ Install robotframework-historic
    ```
    pip install --upgrade robotframework-historic
    ```

 - __Step 2:__ Download and Install MySQL Server - [guide](https://bit.ly/2GrUUZ9)

 - __Step 3:__ Create *rfhistoric* default user with permissions - [guide](https://bit.ly/30ZPT3v)

 - __Step 4:__ Install robotframework-historic-parser
    ```
    pip install --upgrade robotframework-historic-parser
    ```

 - __Step 5:__ Install robotframework-historic-listener
    ```
    pip install --upgrade robotframework-historic-listener
    ```

   > _Note:_ Above all actions are one time activities

---

## How to use in project

 - __Step 1:__ Create project in robotframework-historic - [guide](https://bit.ly/38JskhS)

 - __Step 2:__ Push execution results to project - [guide](https://bit.ly/2U62HUf)

 - __Step 3:__ Open robotframework-historic to view historical results

---

## Existing users:

 - `v0.1.2` new columns are added in `test_results` table

 - Users need to execute following DB script to compatiable with new changes
   ```
   # login to db
   mysql -uroot -p123456

   # select db
   use [projectname];

   # command to add UID column
   ALTER TABLE test_results ADD UID int not null auto_increment primary key AFTER ID;

   # command to add TYPE column
   ALTER TABLE test_results ADD TYPE text AFTER MESSAGE;

   ```

 - Use latest `parser` or `listener` to push data

 > Note: I suggest to create new project, if data is less

---

Thanks for using robotframework-historic

 - What’s your opinion on this report?
 - What’s the feature I should add?

If you have any questions / suggestions / comments on the report, please feel free to reach me at

 - Email: <a href="mailto:adiralashiva8@gmail.com?Subject=Robotframework%20historic" target="_blank">`adiralashiva8@gmail.com`</a>
 - Slack: <a href="https://robotframework.slack.com/messages/robotframeworkhistoric" target="_blank">`robotframeworkhistoric`</a>
 - LinkedIn: <a href="https://www.linkedin.com/in/shivaprasadadirala/" target="_blank">`shivaprasadadirala`</a>
 - Twitter: <a href="https://twitter.com/ShivaAdirala" target="_blank">`@ShivaAdirala`</a>

---

:star: repo if you like it

> Inspired from [ZenQ - ARES Dahsboard](http://www.testastra.com/ares/)

---