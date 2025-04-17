import streamlit as st
import pandas as pd
import plotly.express as px
from Helpers.Database_connectors import (
    get_all_departments,
    get_department_names,
    get_department_employee_count,
    get_budget_distribution,
    add_or_update_department,
    delete_department
)

def main():
    st.set_page_config(page_title="Departments", page_icon="🏢", layout="wide")
    st.title("🏢 Department Overview")
    st.markdown("Gain quick insights into department structures, employee distributions, and budget allocation.")
    st.logo("https://streamlit.io/images/brand/streamlit-mark-color.png")
    
    # --- Pills Navigation ---
    st.markdown("### 📂 Departments")
    dept_names = get_department_names()
    dept_names.insert(0, "All Departments")
    selected = st.pills("Select a Department", options=dept_names, default="All Departments", label_visibility="collapsed")

    # --- KPI Cards ---
    budget_data = pd.DataFrame(get_budget_distribution(), columns=["Name", "Budget"])
    count_data = pd.DataFrame(get_department_employee_count(), columns=["Name", "EmployeeCount"])
    merged_df = pd.merge(count_data, budget_data, on="Name", how="outer").fillna(0)

    if selected != "All Departments":
        merged_df = merged_df[merged_df["Name"] == selected]

    total_employees = int(merged_df["EmployeeCount"].sum())
    total_budget = float(merged_df["Budget"].sum())

    st.markdown("### 📊 Key Metrics")
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="👥 Total Employees", value=f"{total_employees}")
    kpi2.metric(label="💰 Total Budget", value=f"${total_budget:,.2f}")

    # --- Budget Distribution Chart ---
    st.markdown("---")
    st.subheader("💸 Budget Distribution by Department")
    if not budget_data.empty:
        fig_budget = px.pie(
            budget_data,
            names="Name",
            values="Budget",
            title="Share of Total Budget",
            color_discrete_sequence=px.colors.sequential.Tealgrn
        )
        fig_budget.update_traces(textinfo="percent+label", pull=[0.05] * len(budget_data))
        st.plotly_chart(fig_budget, use_container_width=True)
    else:
        st.info("No budget data available.")

    # --- Employee Count Chart ---
    st.markdown("---")
    st.subheader("👥 Employee Count by Department")
    if not count_data.empty:
        fig_count = px.bar(
            count_data,
            x="Name",
            y="EmployeeCount",
            title="Employees per Department",
            text_auto=True,
            color="EmployeeCount",
            color_continuous_scale="Blues"
        )
        fig_count.update_layout(xaxis_title="Department", yaxis_title="Employees")
        st.plotly_chart(fig_count, use_container_width=True)
    else:
        st.info("No employee data available.")

    # --- Add or Update Department Form ---
    st.markdown("---")
    st.subheader("➕ Add or Update Department")
    with st.form("add_update_dept", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            dept_id = st.number_input("Department ID", min_value=1, step=1)
        with col2:
            dept_name = st.text_input("Department Name")
        with col3:
            budget = st.number_input("Budget ($)", min_value=0.0, step=1000.0)

        submitted = st.form_submit_button("💾 Save Department")
        if submitted:
            dept_data = {
                "DeptID": dept_id,
                "Name": dept_name,
                "Budget": budget
            }
            add_or_update_department(dept_data)
            st.success(f"Department '{dept_name}' saved successfully!")

    # --- Delete Department ---
    st.markdown("---")
    st.subheader("🗑️ Delete Department")
    delete_col1, delete_col2 = st.columns([3, 1])
    with delete_col1:
        del_options = get_department_names()
        del_dept = st.selectbox("Choose a department to delete", del_options)
    with delete_col2:
        if st.button("Delete"):
            delete_department(del_dept)
            st.warning(f"Department '{del_dept}' has been deleted.")

if __name__ == "__main__":
    main()
