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

 > Sample Report [Link](https://rfhistoric.netlify.com/)

 > <img src="https://i.ibb.co/KX1bmXs/Dashboard1.png" alt="Overview">

---

## Features

- Support Historic Results
- Visualization of executions
- Search Historical test records by name / status / execution id
- Local hosted (meets privacy concerns)
- Flakiness
- Compare executions
- Generate Robotframework-metrics report
- Custom comments on failures (supports html tags)
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

 - __Step 1:__ Download and Install MySQL Server - [guide](https://bit.ly/2GrUUZ9)

 - __Step 2:__ Install robotframework-historic

    > Case 1: Using pip
    ```
    pip install robotframework-historic==0.1.6
    ```

    > Case 2: Using setup.py (root)
    ```
    python setup.py install
    ```

    > Case 3: Using git (latest changes)
    ```
    pip install git+https://github.com/adiralashiva8/robotframework-historic
    ```

 - __Step 3:__ Create *rfhistoric* default user with permissions - [guide](https://bit.ly/2PIOTfI)

 - __Step 4:__ Create *robothistoric.tb_project* table - [guide](https://bit.ly/2Tv2tV5)

 - __Step 5:__ Install robotframework-historic-parser
    ```
    pip install robotframework-historic-parser==0.1.4
    ```

 - __Step 6:__ Install robotframework-historic-listener
    ```
    pip install robotframework-historic-listener==0.1.4
    ```

   > _Note:_ Above all actions are one time activities

   ### Help / Know More

   To know more on available command refer help
   ```
   rfhistoric --help
   rfhistoricparser --help
   ```

---

## How to use in project

 - __Step 1:__ Create project in robotframework-historic - [guide](https://bit.ly/38JskhS)

 - __Step 2:__ Push execution results to project - [guide](https://bit.ly/2U62HUf)

 - __Step 3:__ Open robotframework-historic to view historical results

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

---
