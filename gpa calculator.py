import streamlit as st
import pandas as pd
import altair as alt

st.title("GPA Calculator")
st.subheader("This is a simple GPA calculator that calculates your GPA based on your marks and credits for each course.\n", divider= "red")
st.subheader("Enter your course details to calculate your GPA")
st.selectbox("Select your year of study", ["<Select>","1st year", "2nd year", "3rd year", "4th year"])
grade_system=st.selectbox("Select your grade system", ["<Select>","Absolute Grading", "Relative Grading"])
scale=st.selectbox("Select your grading scale", ["<Select>","10-point scale", "4-point scale"])
subjects= st.number_input("Enter no. of subjects", min_value=1, max_value=10, step=1)
if grade_system=="Absolute Grading":
    marks=[]
    credits=[]
    grade_points=[]
    with st.form(key="absolute_form"):
        col1, col2 = st.columns(2)
        for i in range(subjects):
            with col1:
                mark=st.number_input(f"Enter your marks for subject {i+1}: ", min_value=0, max_value=100, step=1, key=f"abs_mark_{i}")
            with col2:
                credit=st.number_input(f"Enter your credit for subject {i+1}: ", min_value=0,max_value=10, step=1, key=f"abs_credit_{i}")
            marks.append(mark)
            credits.append(credit)
            factor=0
            if scale=="10-point scale":            factor=1.0
            elif scale=="4-point scale":          factor=0.4
            if mark>=90:
                grade_points.append(10.0*factor)
            elif mark>=80:
                grade_points.append(9.0*factor)
            elif mark>=70:
                grade_points.append(8.0*factor)
            elif mark>=60:
                grade_points.append(7.0*factor)
            elif mark>=50:
                grade_points.append(6.0*factor)
            else:
                grade_points.append(0.0*factor)
        gpa=0
        calculate=st.form_submit_button("Calculate GPA")
    if calculate:
        if grade_system=="<Select>":
            st.warning("Please select a grading system before calculating GPA.")
        elif scale=="<Select>":
            st.warning("Please select a grading scale before calculating GPA.")
        elif sum(credits)==0:
            st.error("Total credits cannot be zero. Please enter valid credits for all subjects.")
        else:
            total_credits = sum(credits)
            for i in range(subjects):
                gpa+=grade_points[i]*credits[i]
            gpa=gpa/total_credits
            st.success(f"Your GPA is: {gpa:.2f}")
            st.divider()
            st.write("**Grade Points per Subject:**")
            df=pd.DataFrame({
                "Subject": [f"Subject {i+1}" for i in range(subjects)],
                "Grade Points": grade_points
            })
            chart=alt.Chart(df).mark_bar(size=40).encode(
                x=alt.X("Subject", sort=None),
                y="Grade Points"
            )
            st.altair_chart(chart, use_container_width=True)
elif grade_system=="Relative Grading":
    st.write("You can predict your GPA based on your expected grade and credit for each course.")
    expected_grades=[]
    credits=[]
    grade_points=[]
    with st.form(key="relative_form"):
        col1, col2 = st.columns(2)
        for i in range(subjects):
            with col1:
                grade=st.selectbox(f"Enter your grade for subject {i+1}: ", options=["<Select>", "S", "A", "B", "C", "D", "E", "F"], key=f"rel_grade_{i}")
            with col2:
                credit=st.number_input(f"Enter your credit for subject {i+1}: ", min_value=0,max_value=10, step=1, key=f"rel_credit_{i}")
            expected_grades.append(grade)
            credits.append(credit)
            factor=0
            if scale=="10-point scale":            factor=1.0
            elif scale=="4-point scale":          factor=0.4
            if grade=="S":
                grade_points.append(10.0*factor)
            elif grade=="A":
                grade_points.append(9.0*factor)
            elif grade=="B":
                grade_points.append(8.0*factor)
            elif grade=="C":
                grade_points.append(7.0*factor)
            elif grade=="D":
                grade_points.append(6.0*factor)
            elif grade=="E":            
                grade_points.append(5.0*factor)
            else:
                grade_points.append(0.0*factor)
        gpa=0
        calculate=st.form_submit_button("Calculate GPA")
    if calculate:
        if grade_system=="<Select>":
            st.warning("Please select a grading system before calculating GPA.")
        elif scale=="<Select>":
            st.warning("Please select a grading scale before calculating GPA.")
        elif "<Select>" in expected_grades:
            st.error("Please select a grade for all subjects.")
        elif sum(credits)==0:
            st.error("Total credits cannot be zero. Please enter valid credits for all subjects.")
        else:
            total_credits=sum(credits)
            for i in range(subjects):
                gpa+=grade_points[i]*credits[i]
            gpa=gpa/total_credits
            st.success(f"Your GPA is: {gpa:.2f}")
            st.info("Note: This GPA is based on your expected grades and may not reflect your actual GPA.")
            st.divider()
            st.write("**Grade Points per Subject:**")
            df=pd.DataFrame({
                "Subject": [f"Subject {i+1}" for i in range(subjects)],
                "Grade Points": grade_points
            })
            chart=alt.Chart(df).mark_bar(size=40).encode(
                x=alt.X("Subject", sort=None),
                y="Grade Points"
            )
            st.altair_chart(chart, use_container_width=True)
