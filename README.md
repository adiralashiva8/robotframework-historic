# robotframework-historic

> MYSQL + FastAPI + Robotframework

![PyPI version](https://badge.fury.io/py/robotframework-historic.svg)
[![Downloads](https://pepy.tech/badge/robotframework-historic)](https://pepy.tech/project/robotframework-historic)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)
[![HitCount](http://hits.dwyl.io/adiralashiva8/robotframework-historic.svg)](http://hits.dwyl.io/adiralashiva8/robotframework-historic)


 > Sample Report (old view) [Link](https://rfhistoric.netlify.com/)

---

### How it Works:

- Get execution details by __parsing__ output.xml
- Store execution results in local / remote hosted __MySQL__ database
- Generate html report from database using __FastAPI__ :zap:

  > <img src="https://i.ibb.co/PzVNGfN/robotframework-historic-overview.png" alt="robotframework-historic-overview">

---

### Requirements

 - Python 3.7 or above
 - MySQL DB

---

### Installation
  > Following steps are one time activity

 - __Step 1:__ Download and Install MySQL Server (follow any one of below approaches) 
    > Case 1: Installing MySql DB in local - [guide](https://bit.ly/2GrUUZ9)
    
    > Case 2: Use the `docker-compose.yml` file to spin up mysql db in docker container.
    
    ```bash
    # spin up mysql db     
    docker-compose up
    ```
    ```bash
    # shutdown mysql db
    docker-compose down
    ```
        
 - __Step 2:__ Install robotframework-historic

    > Case 1: Using pip
    ```
    pip install robotframework-historic==0.2.10
    ```

    > Case 2: Using setup.py (root)
    ```
    python setup.py install
    ```

    > Case 3: Using git (latest changes)
    ```
    pip install git+https://github.com/adiralashiva8/robotframework-historic
    ```

   > Help / Know More
   ```
   rfhistoric --help
   rfhistoricparser --help
   rfhistoricsetup --help
   rfhistoricupdate --help
   ```

 - __Step 3:__ Create *rfhistoric* default user & *robothistoric.TB_PROJECT* table

    > Case 1: Through command line
    ```
    rfhistoricsetup
    ```

    > Case 2: Manual steps
      - Create *rfhistoric* default [guide](https://bit.ly/2PIOTfI)
      - Create *robothistoric.TB_PROJECT* table [guide](https://bit.ly/2Tv2tV5)

  - __Step 4:__ Update database columns (only for existing users with <0.2.5v)

    ```
    rfhistoricupdate
    ```

---

### How to use in project

 - __Step 1:__ Create project in robotframework-historic - [guide](https://bit.ly/38JskhS)

 - __Step 2:__ Push execution results to project - [guide](https://bit.ly/35sSY09)

 - __Step 3:__ Open robotframework-historic to view historical results

---

If you have any questions / suggestions / comments on the report, please feel free to reach me at

 - Email: <a href="mailto:adiralashiva8@gmail.com?Subject=Robotframework%20historic" target="_blank">`adiralashiva8@gmail.com`</a>
 
 - Feedback/Suggestion Form [Link](https://forms.gle/ecdzxQismbPmmYiE6)

---

:star: repo if you like it

---
