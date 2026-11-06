
import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("student_performance.csv")

# Calculate columns
df["Total"] = df[["Maths", "Science", "English"]].sum(axis=1)
df["Average"] = df["Total"] / 3
df["Result"] = df["Average"].apply(
    lambda x: "Pass" if x >= 40 else "Fail"
)

# Dashboard Title
st.title("🎓 Student Performance Analysis Dashboard")
st.write("Analyze student marks, attendance and performance.")

st.divider()

# Sidebar Filter
st.sidebar.header("Student Filters")

gender = st.sidebar.selectbox(
    "Select Gender",
    ["All", "Male", "Female"]
)

if gender == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Gender"] == gender]

# KPI Calculations
total = len(filtered_df)
average = filtered_df["Average"].mean() if total else 0
passed = (filtered_df["Result"] == "Pass").sum()
failed = (filtered_df["Result"] == "Fail").sum()
percentage = (passed / total * 100) if total else 0

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total)
col2.metric("Average Marks", round(average, 2))
col3.metric("Pass Students", passed)
col4.metric("Fail Students", failed)

st.divider()

# Subject-wise Average
st.subheader("📊 Subject-wise Average Marks")

subject_data = pd.DataFrame({
    "Subject": ["Maths", "Science", "English"],
    "Average Marks": [
        filtered_df["Maths"].mean(),
        filtered_df["Science"].mean(),
        filtered_df["English"].mean()
    ]
})

fig1 = px.bar(
    subject_data,
    x="Subject",
    y="Average Marks",
    color="Subject",
    text_auto=".2f",
    title="Average Marks by Subject"
)

st.plotly_chart(fig1, use_container_width=True)

# Pass and Fail Chart
st.subheader("📈 Pass vs Fail Distribution")

result_data = filtered_df["Result"].value_counts().reset_index()
result_data.columns = ["Result", "Students"]

fig2 = px.pie(
    result_data,
    names="Result",
    values="Students",
    hole=0.4
)

st.plotly_chart(fig2, use_container_width=True)

# Attendance Analysis
st.subheader("📚 Attendance vs Average Marks")

fig3 = px.scatter(
    filtered_df,
    x="Attendance",
    y="Average",
    color="Result",
    hover_data=["Student_ID"]
)

st.plotly_chart(fig3, use_container_width=True)

# Top 5 Students
st.subheader("🏆 Top 5 Students")

top_students = filtered_df.sort_values(
    by="Average",
    ascending=False
).head(5)

st.dataframe(top_students, use_container_width=True)

# Complete Student Data
st.subheader("📋 Student Details")

st.dataframe(filtered_df, use_container_width=True)

st.success("Student Performance Dashboard Loaded Successfully!")
