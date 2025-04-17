import streamlit as st
from Helpers.Database_connectors import connect_db, get_dashboard_stats, get_performance_insights
import pandas as pd

# Streamlit UI
def main():
    st.set_page_config(page_title="Employee Dashboard", layout="wide")
    st.logo("https://streamlit.io/images/brand/streamlit-mark-color.png")
    
    st.title("Employee Management Dashboard")
    st.markdown("### Key Metrics & Performance Overview")

    connection = connect_db()
    if not connection:
        st.error("Database connection failed.")
        st.stop()

    # Fetch data
    total_employees, total_departments, active_projects, average_performance = get_dashboard_stats()

    # KPI Cards Layout
    st.markdown("#### Key Performance Indicators")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        st.metric(label="Total Employees", value=total_employees)

    with kpi_col2:
        st.metric(label="Total Departments", value=total_departments)

    with kpi_col3:
        st.metric(label="Active Projects", value=active_projects)

    with kpi_col4:
        st.metric(label="Avg. Performance Score", value=f"{average_performance}%") #, delta= average_performance - 80 if average_performance > 80 else 80 - average_performance

    st.markdown("---")

    top_performers, most_projects, high_success_projects = get_performance_insights()

    # Display Performance Insights
    st.markdown("#### Top 5 Employees with Best Performance")
    if top_performers:
        top_performers_df = pd.DataFrame(top_performers)
        st.dataframe(top_performers_df, use_container_width=True)
    else:
        st.info("No performance data available.")

    st.markdown("#### Employees with Most Projects Assigned")
    if most_projects:
        most_projects_df = pd.DataFrame(most_projects)
        st.dataframe(most_projects_df, use_container_width=True)
    else:
        st.info("No project assignment data available.")

    st.markdown("#### Projects with High Success Rates")
    if high_success_projects:
        high_success_projects_df = pd.DataFrame(high_success_projects)
        st.dataframe(high_success_projects_df, use_container_width=True)
    else:
        st.info("No successful projects data available.")

    connection.close()

if __name__ == "__main__":
    main()
