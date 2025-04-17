import streamlit as st

# Define the pages
Dashboard = st.Page("pages/Dashboard.py", title="Dashboard", icon=":material/dashboard:")
Department = st.Page("pages/Department.py", title="Department Overview", icon=":material/apartment:")
Performance = st.Page("pages/Performance.py", title="Performance Analysis", icon=":material/analytics:")
Projects = st.Page("pages/Projects.py", title="Project Tracking", icon=":material/rocket_launch:")
Employee = st.Page("pages/Employee.py", title="Employee Management", icon=":material/folder_open:")

pages = {
    "Main" : [
        Dashboard
    ],
    "Metrics":[
        Employee,
        Performance,
        Department,
        Projects
    ],
}
# Set up navigation
pg = st.navigation(pages)

# Run the selected page
pg.run()