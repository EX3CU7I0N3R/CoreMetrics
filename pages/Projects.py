import streamlit as st
import pandas as pd
import plotly.express as px
from Helpers.Database_connectors import (
    get_all_projects,
    get_project_performance,
    get_top_projects,
    get_underperforming_projects,
    bulk_insert_project_performance
)

def main():
    st.set_page_config(page_title="Project Tracker", page_icon=":bar_chart:")
    st.title("📋 Project Tracking Dashboard")
    st.markdown("Monitor project progress, success rates, and performance metrics across all departments.")
    st.logo("https://streamlit.io/images/brand/streamlit-mark-color.png")
    
    st.divider()

    # ====================================================
    # 📌 Project KPIs
    # ====================================================
    st.subheader("📌 Key Project Metrics")

    all_projects = pd.DataFrame(
        get_all_projects(),
        columns=["ProjectID", "EmployeeID", "ProjectInfo", "SuccessIndicator"]
    )

    total_projects = len(all_projects)
    status_counts = all_projects['SuccessIndicator'].value_counts()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Projects", total_projects)
    col2.metric("Completed", status_counts.get("Completed on time", 0))
    col3.metric("In Progress", status_counts.get("In Progress", 0))
    col4.metric("Pending", total_projects - (status_counts.get("Completed on time", 0)+status_counts.get("In Progress", 0)))

    st.divider()    

    # ====================================================
    # 🧭 Project Status Distribution
    # ====================================================
    st.subheader("🧭 Project Status Distribution")

    fig_status = px.pie(
        all_projects,
        names="SuccessIndicator",
        title="Project Completion Breakdown",
        hole=0.4
    )
    st.plotly_chart(fig_status, use_container_width=True)

    st.divider()

    # ====================================================
    # 🗂️ Filterable Project Table
    # ====================================================
    st.subheader("🗂️ View & Filter Projects")

    filter_status = st.selectbox("Filter by Status", options=["All"] + list(status_counts.index))
    filtered_projects = all_projects if filter_status == "All" else all_projects[all_projects["SuccessIndicator"] == filter_status]
    st.dataframe(filtered_projects, use_container_width=True)

    st.divider()

    # ====================================================
    # 📈 Performance Metrics per Project
    # ====================================================
    st.subheader("📈 Project Performance Overview")

    performance_data = pd.DataFrame(
        get_project_performance(),
        columns=["ProjectID", "ProjectInfo", "EfficiencyScore", "TimelineScore", "QualityScore", "AccuracyScore"]
    )

    if not performance_data.empty:
        performance_data["AvgScore"] = performance_data[
            ["EfficiencyScore", "TimelineScore", "QualityScore", "AccuracyScore"]
        ].mean(axis=1)

        fig_perf = px.bar(
            performance_data,
            x="ProjectInfo",
            y="AvgScore",
            color="AvgScore",
            title="Average Performance by Project",
            text_auto=True
        )
        st.plotly_chart(fig_perf, use_container_width=True)
    else:
        st.info("No project performance data available at the moment.")

    st.divider()

    # ====================================================
    # 🏆 Top Performing Projects
    # ====================================================
    st.subheader("🏆 Top Performing Projects")

    top_projects = pd.DataFrame(get_top_projects())
    if not top_projects.empty:
        st.dataframe(top_projects, use_container_width=True)
    else:
        st.info("No top-performing projects found.")

    st.divider()

    # ====================================================
    # ⚠️ Underperforming Projects
    # ====================================================
    st.subheader("⚠️ Underperforming Projects")

    under_projects = pd.DataFrame(get_underperforming_projects())
    if not under_projects.empty:
        st.dataframe(under_projects, use_container_width=True)
    else:
        st.success("All projects are currently performing above the defined threshold.")

    st.divider()

    # ====================================================
    # 📤 Upload Performance Data
    # ====================================================
    st.subheader("📤 Upload Project Performance Data")

    st.markdown(
        """
        Upload a CSV file containing the following columns:
        **EmpID, ProjectID, AccuracyScore, EfficiencyScore, QualityScore, TimelineScore**
        """
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        upload_df = pd.read_csv(uploaded_file)
        st.dataframe(upload_df)

        if st.button("🚀 Upload Data"):
            if bulk_insert_project_performance(upload_df):
                st.success("Performance data uploaded successfully.")
            else:
                st.error("Upload failed. Please verify the CSV format and try again.")

if __name__ == "__main__":
    main()
