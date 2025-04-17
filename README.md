# CoreMetrics

**CoreMetrics** is a robust Streamlit-based web dashboard for comprehensive employee and project performance monitoring. It integrates seamlessly with a MySQL backend to provide real-time analytics, KPIs, project tracking, and performance management in an intuitive interface.

## 📚 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Database Schema](#-database-schema)
- [Setup Instructions](#%EF%B8%8F-setup-instructions)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)

---

## ✅ Features

- **Unified Dashboard for Project Monitoring**  
  Gain a centralized view of all ongoing, completed, and pending projects with real-time status indicators and performance breakdowns.

- **KPI-Driven Analytics**  
  Track key performance indicators such as project completion rates, departmental success distribution, and individual performance scores.

- **Interactive Visualizations**  
  Leverage dynamic charts powered by Plotly to explore project success trends, performance metrics, and comparative analytics.

- **Department and Employee Insights**  
  View and manage department-level data, including total employee counts, budget allocations, and inter-departmental performance comparisons.

- **Evaluator and Review Mechanism**  
  Identify and associate evaluators with employees, supporting multi-level review processes and accountability tracking.

- **CSV-Based Bulk Upload**  
  Quickly update performance data with support for CSV upload, allowing seamless integration of external analytics pipelines.

- **Advanced Filtering and Drill-Down**  
  Filter records by status, department, or project success rate to isolate underperforming segments or top achievers.

- **Modular and Scalable Design**  
  Built on a modular architecture, CoreMetrics allows for easy integration of additional modules such as audit logs, role-based access, or time-based analytics.

- **Streamlit-Powered Interface**  
  A responsive, lightweight UI using Streamlit for rapid development, minimal overhead, and cloud deployment readiness.

- **BCNF-Normalized Database**  
  Optimized database schema adhering to Boyce–Codd Normal Form ensures data integrity, efficient querying, and minimal redundancy.

---

## 🛠 Tech Stack

### 🔹 Frontend
- **Streamlit**  
  Utilized for rapid development of interactive, data-driven dashboards with minimal boilerplate. Streamlit provides seamless integration with Python, enabling clean UI/UX for monitoring and visual analysis.

- **Plotly Express**  
  Used for generating high-quality, interactive visualizations, including bar charts, pie charts, and performance graphs to enhance data interpretation.

### 🔹 Backend
- **Python**  
  Core programming language used for data processing, database communication, and backend logic implementation.

- **MySQL**  
  Relational database management system used for storing normalized project, employee, performance, and evaluation data. The schema is designed to comply with Boyce–Codd Normal Form (BCNF) for optimal efficiency.

- **Pandas**  
  Employed for data manipulation, transformation, and loading CSV datasets for performance evaluation.

### 🔹 Database Interface
- **Custom Helper Module (`Helpers/Database_connectors.py`)**  
  Encapsulates all MySQL query logic and connection management, maintaining separation of concerns and ensuring code modularity.

### 🔹 Data Formats
- **CSV (Comma-Separated Values)**  
  Supported for bulk uploads of performance data, allowing administrators to update large datasets efficiently.

---

## 🗂 Database Schema

The `CoreMetrics` database is structured to ensure data integrity, scalability, and performance tracking accuracy. The schema is fully normalized to **Boyce–Codd Normal Form (BCNF)**, minimizing redundancy and optimizing relational consistency.

### 1. `employee`
Stores information about all employees in the organization.

| Column Name   | Data Type     | Description                        |
|---------------|----------------|------------------------------------|
| EmpID         | INT (PK)       | Unique identifier for each employee |
| Name          | VARCHAR(100)   | Full name of the employee           |
| DeptID        | INT (FK)       | Foreign key referencing `department` |
| AttendanceID  | INT            | Employee’s attendance tracking ID   |
| EmailID       | VARCHAR(100)   | Official email address              |
| DOB           | DATE           | Date of birth                       |
| Address       | TEXT           | Residential address                 |
| WorkEx        | FLOAT          | Total years of work experience      |
| Salary        | DECIMAL(10,2)  | Monthly salary                      |

---

### 2. `department`
Represents all departments in the organization.

| Column Name | Data Type     | Description                         |
|-------------|----------------|-------------------------------------|
| DeptID      | INT (PK)       | Unique department identifier        |
| Name        | VARCHAR(100)   | Department name                     |

---

### 3. `project`
Captures project assignment and status.

| Column Name       | Data Type     | Description                                      |
|-------------------|----------------|--------------------------------------------------|
| ProjectID         | INT (PK)       | Unique identifier for each project              |
| EmployeeID        | INT (FK)       | References the employee leading the project     |
| ProjectInfo       | TEXT           | Description or summary of the project           |
| SuccessIndicator  | VARCHAR(50)    | Project status (e.g., Completed, In Progress)   |

---

### 4. `performance`
Contains detailed performance metrics per employee per project.

| Column Name      | Data Type     | Description                                   |
|------------------|----------------|-----------------------------------------------|
| PerformanceID    | INT (PK)       | Unique performance entry ID                   |
| EmpID            | INT (FK)       | References `employee`                         |
| ProjectID        | INT (FK)       | References `project`                          |
| EfficiencyScore  | FLOAT          | Score representing efficiency                 |
| TimelineScore    | FLOAT          | Score based on project timeline adherence     |
| QualityScore     | FLOAT          | Score measuring output quality                |
| AccuracyScore    | FLOAT          | Accuracy rating of deliverables               |

---

### 5. `evaluator`
Links evaluators to employees they are assigned to evaluate.

| Column Name  | Data Type   | Description                          |
|--------------|--------------|--------------------------------------|
| EvaluatorID  | INT (PK)     | Unique ID for evaluator              |
| EmpID        | INT (FK)     | Employee being evaluated             |


---

## 🛠️ Setup Instructions

Follow the steps below to set up and run the **CoreMetrics** project on your local development environment.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CoreMetrics.git
cd CoreMetrics
```

---

### 2. Set Up the Python Environment

Ensure you have **Python 3.8+** installed. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

### 3. Configure the MySQL Database

1. **Start your MySQL server.**
2. **Create a new database** named `coremetrics` (or any name of your choice).
3. **Import the SQL dump** to create all tables and insert sample data:

```bash
mysql -u root -p coremetrics < load.sql
```

To avoid hardcoding credentials, use a `.env` file to store your database configuration:

```bash
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=coremetrics
```

---

### 4. Launch the Streamlit App

Run the main dashboard:

```bash
streamlit run main.py
```

This will start the CoreMetrics dashboard in your browser at [http://localhost:8501](http://localhost:8501).

---

## 🖼️ Screenshots
*(Comming soon...)*

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss proposed changes.

---
