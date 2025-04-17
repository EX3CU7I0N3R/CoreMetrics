import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

"""

# Get Column Names for a Table
def get_columns(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Fetch column names dynamically
        cursor.execute(f"SHOW COLUMNS FROM {table_name};")
        columns = [column[0] for column in cursor.fetchall()]
        
        conn.close()
        return columns
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

# Create or Update a Record (Generic for Any Table)
def create_or_update_record(table_name, record_data):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        columns = get_columns(table_name)
        if not columns:
            print(f"Table {table_name} not found.")
            return

        keys = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        update_clause = ", ".join([f"{col} = VALUES({col})" for col in columns])

        query = f"""
        # INSERT INTO {table_name} ({keys}) 
        # VALUES ({placeholders})
        # ON DUPLICATE KEY UPDATE {update_clause};
"""
        
        values = tuple(record_data.get(col, None) for col in columns)
        cursor.execute(query, values)
        conn.commit()
        
        print(f"Record inserted/updated in {table_name}.")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Delete a Record by Primary Key
def delete_record(table_name, column, value):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = f"DELETE FROM {table_name} WHERE {column} = %s;"
        cursor.execute(query, (value,))
        conn.commit()

        print(f"Record with {column} = {value} deleted from {table_name}.")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
"""
# Function to fetch dashboard stats
def get_dashboard_stats():
    conn = connect_db()
    cursor = conn.cursor()

    # Queries for key metrics
    cursor.execute("SELECT COUNT(*) FROM employee;")
    total_employees = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT DeptID) FROM employee;")
    total_departments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM project WHERE SuccessIndicator = 'In Progress';")
    active_projects = cursor.fetchone()[0]

    cursor.execute("SELECT AVG((AccuracyScore + EfficiencyScore + QualityScore + TimelineScore) / 4) FROM performance;")
    average_performance = round(cursor.fetchone()[0], 2)

    conn.close()

    return total_employees, total_departments, active_projects, average_performance

# Function to fetch performance insights
def get_performance_insights():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ Top 5 Employees with Best Performance (Average Score)
    cursor.execute("""
        SELECT e.EmpID, e.Name, ROUND(AVG((p.AccuracyScore + p.EfficiencyScore + p.QualityScore + p.TimelineScore) / 4), 2) AS AvgScore
        FROM performance p
        JOIN employee e ON p.EmpID = e.EmpID
        GROUP BY e.EmpID, e.Name
        ORDER BY AvgScore DESC
        LIMIT 5;
    """)
    top_performers = cursor.fetchall()

    # 2️⃣ Employees with Most Projects Assigned
    cursor.execute("""
        SELECT e.EmpID, e.Name, COUNT(pr.ProjectID) AS TotalProjects
        FROM project pr
        JOIN employee e ON pr.EmployeeID = e.EmpID
        GROUP BY e.EmpID, e.Name
        ORDER BY TotalProjects DESC
        LIMIT 5;
    """)
    most_projects = cursor.fetchall()

    # 3️⃣ Projects with High Success Rates
    cursor.execute("""
        SELECT ProjectID, ProjectInfo, SuccessIndicator
        FROM project
        WHERE SuccessIndicator = 'Completed on time'
        ORDER BY ProjectID ASC
        LIMIT 5;
    """)
    high_success_projects = cursor.fetchall()

    conn.close()

    return top_performers, most_projects, high_success_projects

"""
Employee.py
"""
# View All Records from Any Table
def view_records(table_name):
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        
        # Fetch all records
        cursor.execute(f"SELECT * FROM {table_name};")
        records = cursor.fetchall()

        # Convert to Pandas DataFrame
        df = pd.DataFrame(records)

        conn.close()

        # Return DataFrame
        return df if not df.empty else pd.DataFrame(columns=["No records found"])
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return pd.DataFrame(columns=["Error"])

def create_or_update_employee(emp_data):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO employee (EmpID, DeptID, AttendanceID, EmailID, DOB, Address, WorkEx, Salary, Name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            DeptID=VALUES(DeptID),
            AttendanceID=VALUES(AttendanceID),
            EmailID=VALUES(EmailID),
            DOB=VALUES(DOB),
            Address=VALUES(Address),
            WorkEx=VALUES(WorkEx),
            Salary=VALUES(Salary),
            Name=VALUES(Name);
        """

        cursor.execute(query, (
            emp_data['EmpID'],
            emp_data['DeptID'],
            emp_data['AttendanceID'],
            emp_data['EmailID'],
            emp_data['DOB'],
            emp_data['Address'],
            emp_data['WorkEx'],
            emp_data['Salary'],
            emp_data['Name']
        ))

        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False


# Delete Employee Record

def delete_employee(emp_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM employee WHERE EmpID = %s", (emp_id,))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False


# Get All Employee IDs for Dropdown

def get_employee_ids():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT EmpID FROM employee")
        ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ids
    except:
        return []

"""
Performance.py
"""
def get_all_performance_records():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT e.EmpID, e.Name, p.ProjectID, 
               p.EfficiencyScore, p.TimelineScore, 
               p.QualityScore, p.AccuracyScore
        FROM performance p
        JOIN employee e ON p.EmpID = e.EmpID;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def get_performance_averages():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            ROUND(AVG(EfficiencyScore), 2),
            ROUND(AVG(TimelineScore), 2),
            ROUND(AVG(QualityScore), 2),
            ROUND(AVG(AccuracyScore), 2)
        FROM performance;
    """)
    averages = cursor.fetchone()
    conn.close()

    return {
        "Efficiency": averages[0],
        "Timeline": averages[1],
        "Quality": averages[2],
        "Accuracy": averages[3],
    }

def get_top_performers(limit=5):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
        SELECT e.EmpID, e.Name, 
               ROUND(AVG((p.EfficiencyScore + p.TimelineScore + p.QualityScore + p.AccuracyScore)/4), 2) AS AvgScore
        FROM performance p
        JOIN employee e ON p.EmpID = e.EmpID
        GROUP BY e.EmpID, e.Name
        ORDER BY AvgScore DESC
        LIMIT {limit};
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def get_underperformers(threshold=60):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
        SELECT e.EmpID, e.Name, 
               ROUND(AVG((p.EfficiencyScore + p.TimelineScore + p.QualityScore + p.AccuracyScore)/4), 2) AS AvgScore
        FROM performance p
        JOIN employee e ON p.EmpID = e.EmpID
        GROUP BY e.EmpID, e.Name
        HAVING AvgScore < {threshold}
        ORDER BY AvgScore ASC;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def bulk_insert_performance(df):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO performance (EmpID, ProjectID, AccuracyScore, EfficiencyScore, QualityScore, TimelineScore)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    AccuracyScore=VALUES(AccuracyScore),
                    EfficiencyScore=VALUES(EfficiencyScore),
                    QualityScore=VALUES(QualityScore),
                    TimelineScore=VALUES(TimelineScore);
            """, tuple(row))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Bulk insert error: {e}")
        return False

def get_analytics():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT e.EmpID, e.Name, 
               ROUND(AVG((AccuracyScore + EfficiencyScore + QualityScore + TimelineScore)/4), 2) AS AvgScore
        FROM performance p
        JOIN employee e ON p.EmpID = e.EmpID
        GROUP BY e.EmpID, e.Name
        ORDER BY AvgScore DESC
        LIMIT 3;
    """)
    top_employees = cursor.fetchall()

    cursor.execute("""
        SELECT e.EmpID, e.Name, 
               ROUND(AVG((AccuracyScore + EfficiencyScore + QualityScore + TimelineScore)/4), 2) AS AvgScore
        FROM performance p
        JOIN employee e ON p.EmpID = e.EmpID
        GROUP BY e.EmpID, e.Name
        ORDER BY AvgScore ASC
        LIMIT 3;
    """)
    low_employees = cursor.fetchall()

    conn.close()
    return top_employees, low_employees

def filter_performance(dept_id=None, project_id=None):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT e.EmpID, e.Name, e.DeptID, p.ProjectID, 
               ROUND((p.AccuracyScore + p.EfficiencyScore + p.QualityScore + p.TimelineScore)/4, 2) AS AvgScore
        FROM performance p
        JOIN employee e ON p.EmpID = e.EmpID
        WHERE 1=1
    """
    params = []

    if dept_id:
        query += " AND e.DeptID = %s"
        params.append(dept_id)

    if project_id:
        query += " AND p.ProjectID = %s"
        params.append(project_id)

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    conn.close()
    return data


"""
Department.py
"""

def get_all_departments():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM department")
    data = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    connection.close()
    return [dict(zip(columns, row)) for row in data]

def get_department_names():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT Name FROM department")
    names = [row[0] for row in cursor.fetchall()]
    connection.close()
    return names

def get_department_employee_count():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT d.Name, COUNT(e.EmpID) AS Count FROM department d LEFT JOIN employee e ON d.DeptID = e.DeptID GROUP BY d.Name")
    data = cursor.fetchall()
    connection.close()
    return data

def get_budget_distribution():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT d.Name, SUM(e.Salary) AS Budget
        FROM department d
        JOIN employee e ON d.DeptID = e.DeptID
        GROUP BY d.Name
    """)
    return cursor.fetchall()


def add_or_update_department(dept_data):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO department (DeptID, Name, Budget, Head)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        Name = VALUES(Name),
        Budget = VALUES(Budget),
        Head = VALUES(Head)
    """, (dept_data['DeptID'], dept_data['Name'], dept_data['Budget'], dept_data['Head']))
    connection.commit()
    connection.close()

def delete_department(dept_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM department WHERE DeptID = %s", (dept_id,))
    connection.commit()
    connection.close()


"""
Projects.py
"""


def get_all_projects():
    connection = connect_db()
    cursor = connection.cursor()
    query = "SELECT * FROM project"
    cursor.execute(query)
    return cursor.fetchall()

def get_project_performance():
    connection = connect_db()
    cursor = connection.cursor()
    query = """
        SELECT p.ProjectID, pr.ProjectInfo,
               ROUND(AVG(EfficiencyScore), 2) AS AvgEfficiency,
               ROUND(AVG(TimelineScore), 2) AS AvgTimeline,
               ROUND(AVG(QualityScore), 2) AS AvgQuality,
               ROUND(AVG(AccuracyScore), 2) AS AvgAccuracy
        FROM performance p
        JOIN project pr ON p.ProjectID = pr.ProjectID
        GROUP BY p.ProjectID, pr.ProjectInfo
    """
    cursor.execute(query)
    return cursor.fetchall()


def get_top_projects(threshold=85):
    connection = connect_db()
    cursor = connection.cursor()
    query = """
        SELECT pr.ProjectID, pr.ProjectInfo,
               ROUND(AVG((EfficiencyScore + TimelineScore + QualityScore + AccuracyScore)/4), 2) AS AvgScore
        FROM performance p
        JOIN project pr ON p.ProjectID = pr.ProjectID
        GROUP BY pr.ProjectID, pr.ProjectInfo
        HAVING AvgScore >= %s
        ORDER BY AvgScore DESC
    """
    cursor.execute(query, (threshold,))
    return cursor.fetchall()

def get_underperforming_projects(threshold=70):
    connection = connect_db()
    cursor = connection.cursor()
    query = """
        SELECT pr.ProjectID, pr.ProjectInfo,
               ROUND(AVG((EfficiencyScore + TimelineScore + QualityScore + AccuracyScore)/4), 2) AS AvgScore
        FROM performance p
        JOIN project pr ON p.ProjectID = pr.ProjectID
        GROUP BY pr.ProjectID, pr.ProjectInfo
        HAVING AvgScore < %s
        ORDER BY AvgScore ASC
    """
    cursor.execute(query, (threshold,))
    return cursor.fetchall()

def bulk_insert_project_performance(df):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO performance (EmpID, ProjectID, EfficiencyScore, TimelineScore, QualityScore, AccuracyScore)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = [
            (
                row["EmpID"], row["ProjectID"],
                row["EfficiencyScore"], row["TimelineScore"],
                row["QualityScore"], row["AccuracyScore"]
            )
            for _, row in df.iterrows()
        ]
        cursor.executemany(query, data)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error uploading project performance: {e}")
        return False
