import streamlit as st
import pandas as pd
import plotly.express as px
from Helpers.Database_connectors import (
    get_all_performance_records,
    bulk_insert_performance,
    get_performance_averages,
    get_top_performers,
    get_underperformers,
    filter_performance    
)

def main():
    st.set_page_config(page_title="Performance Insights", page_icon="📊", layout="wide")
    st.title("📊 Employee Performance Dashboard")
    st.markdown("Analyze individual and team performance trends to make informed organizational decisions.")
    st.logo("https://streamlit.io/images/brand/streamlit-mark-color.png")
    
    st.divider()

    # ================================
    # 🎯 Filter Performance Records
    # ================================
    st.subheader("🎯 Filter Records by Department or Project")
    with st.expander("Apply filters", expanded=True):
        col1, col2 = st.columns(2)
        dept_input = col1.text_input("Department ID", placeholder="e.g., D001")
        proj_input = col2.text_input("Project ID", placeholder="e.g., P105")

        if st.button("🔍 Filter Records"):
            filtered = filter_performance(dept_input or None, proj_input or None)
            df_filtered = pd.DataFrame(filtered)

            if df_filtered.empty:
                st.warning("No matching performance records found.")
            else:
                st.success(f"Displaying {len(df_filtered)} filtered performance records.")
                st.dataframe(df_filtered, use_container_width=True)

                fig = px.bar(
                    df_filtered,
                    x="Name",
                    y="AvgScore",
                    color="AvgScore",
                    color_continuous_scale="Viridis",
                    title="Filtered Employee Performance Overview",
                    text_auto=True
                )
                fig.update_layout(xaxis_title="Employee", yaxis_title="Average Score")
                st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ================================
    # 📈 Performance Averages Overview
    # ================================
    st.subheader("📈 Performance Averages Across Categories")
    averages = get_performance_averages()
    avg_df = pd.DataFrame({
        "Metric": list(averages.keys()),
        "Average Score": list(averages.values())
    })

    fig_avg = px.bar(
        avg_df,
        x="Metric",
        y="Average Score",
        color="Metric",
        text_auto=True,
        title="Average Scores by Metric",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    fig_avg.update_layout(yaxis_range=[0, 10], yaxis_title="Score (out of 10)")
    st.plotly_chart(fig_avg, use_container_width=True)

    st.divider()

    # ================================
    # 🏅 Top Performers
    # ================================
    st.subheader("🏅 Top Performing Employees")
    top_df = pd.DataFrame(get_top_performers())

    if not top_df.empty:
        st.dataframe(top_df, use_container_width=True)

        fig_top = px.bar(
            top_df,
            x="Name",
            y="AvgScore",
            color="Name",
            text="AvgScore",
            title="Top Performers",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_top.update_layout(xaxis_title="Employee", yaxis_title="Average Score")
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("No top performers identified at this time.")

    st.divider()

    # ================================
    # ⚠️ Underperformers
    # ================================
    st.subheader("⚠️ Employees Requiring Attention")
    under_df = pd.DataFrame(get_underperformers())

    if not under_df.empty:
        st.dataframe(under_df, use_container_width=True)

        fig_under = px.bar(
            under_df,
            x="Name",
            y="AvgScore",
            color="Name",
            text="AvgScore",
            title="Underperformers",
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_under.update_layout(xaxis_title="Employee", yaxis_title="Average Score")
        st.plotly_chart(fig_under, use_container_width=True)
    else:
        st.success("All employees meet the minimum performance threshold.")

    st.divider()

    # ================================
    # 📁 Upload Performance CSV
    # ================================
    st.subheader("📁 Upload Performance Data")
    st.markdown("""
        Upload a `.csv` file with the following **required columns**:
        - `EmpID`
        - `ProjectID`
        - `AccuracyScore`
        - `EfficiencyScore`
        - `QualityScore`
        - `TimelineScore`
    """)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.dataframe(df_upload, use_container_width=True)

        if st.button("🚀 Upload Data"):
            success = bulk_insert_performance(df_upload)
            if success:
                st.success("Performance data uploaded successfully!")
            else:
                st.error("Upload failed. Please check your file format and data consistency.")

if __name__ == "__main__":
    main()
