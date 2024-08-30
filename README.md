<div align="center">
  <h1>Robot Framework Historic</h1>
  <p>
      Custom HTML report that tracks historical Robot Framework test results using MySQL and Flask
  </p>

<!-- Badges -->
<p>
  <a href="https://github.com/adiralashiva8/robotframework-historic/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/adiralashiva8/robotframework-historic" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/adiralashiva8/robotframework-historic" alt="last update" />
  </a>
  <a href="https://github.com/adiralashiva8/robotframework-historic/network/members">
    <img src="https://img.shields.io/github/forks/adiralashiva8/robotframework-historic" alt="forks" />
  </a>
  <a href="https://github.com/adiralashiva8/robotframework-historic/stargazers">
    <img src="https://img.shields.io/github/stars/adiralashiva8/robotframework-historic" alt="stars" />
  </a>
  <a href="https://github.com/adiralashiva8/robotframework-historic/issues/">
    <img src="https://img.shields.io/github/issues/adiralashiva8/robotframework-historic" alt="open issues" />
  </a>
  <a href="https://github.com/adiralashiva8/robotframework-historic/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/adiralashiva8/robotframework-historic.svg" alt="license" />
  </a>
</p>

<h4>
    <a href="https://github.com/adiralashiva8/robotframework-historic/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/adiralashiva8/robotframework-historic/blob/master/README.md">Documentation</a>
  <span> · </span>
    <a href="https://github.com/adiralashiva8/robotframework-historic/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/adiralashiva8/robotframework-historic/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->
# 📔 Table of Contents

- [About the Project](#-about-the-project)
  * [Screenshots](#-screenshots)
  * [Tech Stack](#-tech-stack)
  * [Features](#-features)
  * [How It Works](#-works)
- [Getting Started](#-getting-started)
  * [Installation](#-installation)
- [Usage](#-usage)
  * [Continuous Integration (CI) Setup](#-cisetup)
- [Contact](#-contact)
- [Acknowledgements](#-acknowledgements)

<!-- About the Project -->
## 🌟 About the Project

`Robot Framework Historic` is a comprehensive tool designed to help you visualize the `historical` results of your Robot Framework tests. By storing execution results in a `MySQL` database and generating `HTML` reports with Flask, it provides a detailed overview of your testing history, complete with charts and statistical insights.

<!-- Screenshots -->
### 📷 Screenshots

<div align="center">
  <img src="https://i.ibb.co/dmVjkMC/historic.png" alt="screenshot" />
</div>

<!-- TechStack -->
### 🛠️ Tech Stack

<details>
  <ul>
    <li><a href="https://www.python.org/">Python</a></li>
    <li><a href="https://robot-framework.readthedocs.io/en/stable/autodoc/robot.result.html">MySQL Database</a></li>
    <li><a href="https://flask.palletsprojects.com/en/3.0.x/">Flask</a></li>
  </ul>
</details>

<!-- Features -->
### 🎯 Features

- *Latest Results Overview*
- *Recent Execution Trends (5, 10, 30 Days)*
- *Flaky Test Identification*
- *Search Test History by Name*
- *Side-by-Side Execution Comparison*
- *Analysis & Comments on Test Executions*

### 🛠️ How It Works

 - *Parse Execution Details:* Parses the output.xml to extract detailed execution results
 - *Store Results:* These results are then stored in either a local or remotely hosted MySQL database
 - *Generate Reports:* Using Flask, the stored data is transformed into comprehensive HTML reports

  <div align="center">
    <img src="https://i.ibb.co/PzVNGfN/robotframework-historic-overview.png" alt="robotframework-historic-overview" />
  </div>


<!-- Getting Started -->
## 🧰 Getting Started

<!-- Installation -->
### ⚙️ Installation

Setting up `robotframework-historic` is a one-time activity. Just follow these steps:

__Step 1:__ Install MySQL
 - MySQL Setup: [Guide](https://github.com/adiralashiva8/robotframework-historic/wiki/1.-MySQL-Setup-Guide)
 - MySQL User Setup: [Guide](https://github.com/adiralashiva8/robotframework-historic/wiki/2.1-Create-MySQL-User)

__Step 2:__ Install robotframework-historic
  ```
  pip install git+https://github.com/adiralashiva8/robotframework-historic
  ```

__Step 3:__ Set Up the Database
 - CLI: `rfhistoricsetup`
 - Manual: [Guide](https://github.com/adiralashiva8/robotframework-historic/wiki/2.2-Create-robothistoric-table)


<!-- Usage -->
## 👀 Usage

__Step 1:__ Create a New Project: [Guide](https://github.com/adiralashiva8/robotframework-historic/wiki/3.-Create-Project-In-RF-Historic)

__Step 2:__ Push Test Results: [Guide](https://github.com/adiralashiva8/robotframework-historic/wiki/4.-Push-robotframework-execution-results-to-MySQL)

__Step 3:__ View Reports: Open in browser

*Encountering MySQL issues?* Try installing these dependencies:
```
pip install mysql-connector-python
pip install PyMySQL
```

For more options:
```
rfhistoric --help
rfhistoricparser --help
rfhistoricsetup --help
rfhistoricupdate --help
```

### 🧪 Continuous Integration (CI) Setup

To automate report generation in CI/CD pipelines, add the following steps to your pipeline configuration:

1. Run tests with Robot Framework
2. push results to dB
   ```
   robot test.robot &
   rfhistoricparser [:options]
   ```
   > & is used to execute multiple command's in .bat file

<!-- Contact -->
## 🤝 Contact

For any questions, suggestions, or feedback, please contact:

- Email: <a href="mailto:adiralashiva8@gmail.com?Subject=Robotframework%20Historic" target="_blank">`adiralashiva8@gmail.com`</a>

<!-- Acknowledgments -->
## 💎 Acknowledgements

1. [Robotframework community users](https://groups.google.com/forum/#!forum/robotframework-users)

---

⭐ Star this repository if you find it useful! (it motivates)

---
