import streamlit as st
import plotly.express as px
from Helpers.Database_connectors import (
    view_records,
    create_or_update_employee,
    delete_employee,
    get_employee_ids
)

def main():
    st.set_page_config(page_title="Employee Management", page_icon=":material/monitoring:", layout="wide")
    st.title("Employee Management Dashboard")
    st.markdown("Manage, analyze, and gain insights into employee data.")
    st.logo("https://streamlit.io/images/brand/streamlit-mark-color.png")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 View Employees", "➕ Add/Update Employee", "❌ Delete Employee"])

    # ============================
    # 📋 TAB 1: View Employees
    # ============================
    with tab1:
        df = view_records("employee")
        st.markdown("### Employee Directory")
        st.dataframe(df, use_container_width=True)


    # ============================
    # ➕ TAB 2: Add or Update Employee
    # ============================
    with tab2:
        st.markdown("### Add or Update Employee Record")
        with st.form("employee_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                emp_id = st.number_input("Employee ID", min_value=1, step=1)
                name = st.text_input("Full Name")
                dept_id = st.number_input("Department ID", min_value=1, step=1)
                attendance_id = st.number_input("Attendance ID", min_value=1, step=1)
                email = st.text_input("Email ID")
            with col2:
                dob = st.date_input("Date of Birth")
                address = st.text_area("Address")
                work_ex = st.number_input("Work Experience (Years)", min_value=0, step=1)
                salary = st.number_input("Salary", min_value=0.0, step=500.0)

            submit = st.form_submit_button("💾 Save Employee")

        if submit:
            emp_data = {
                "EmpID": emp_id,
                "Name": name,
                "DeptID": dept_id,
                "AttendanceID": attendance_id,
                "EmailID": email,
                "DOB": dob.strftime("%Y-%m-%d"),
                "Address": address,
                "WorkEx": work_ex,
                "Salary": salary
            }
            create_or_update_employee(emp_data)
            st.success("✅ Employee record successfully saved or updated.")

    # ============================
    # ❌ TAB 3: Delete Employee
    # ============================
    with tab3:
        st.markdown("### Delete an Employee Record")
        emp_ids = get_employee_ids()
        if emp_ids:
            emp_to_delete = st.selectbox("Select Employee ID to delete", emp_ids)
            if st.button("⚠️ Confirm Deletion"):
                delete_employee(emp_to_delete)
                st.warning(f"🚫 Employee {emp_to_delete} has been removed from the system.")
        else:
            st.info("No employees available to delete.")
    if not df.empty:
        st.markdown("---")
        st.markdown("### Workforce Insights")
        col1, col2 = st.columns(2)

        with col1:
            if "DeptID" in df.columns:
                dept_count = df["DeptID"].value_counts().reset_index()
                dept_count.columns = ["DeptID", "Count"]
                fig1 = px.pie(dept_count, names='DeptID', values='Count', title="Department-wise Distribution")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if "WorkEx" in df.columns:
                fig2 = px.histogram(df, x="WorkEx", nbins=10, title="Work Experience Distribution (Years)")
                st.plotly_chart(fig2, use_container_width=True)
        st.markdown("### Salary Analysis")
        if "Salary" in df.columns:
            fig3 = px.histogram(df, x="Salary", nbins=20, title="Employee Salary Distribution")
            st.plotly_chart(fig3, use_container_width=True)


if __name__ == "__main__":
    main()
