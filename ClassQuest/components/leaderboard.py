import streamlit as st
import plotly.express as px

def display_student_stats(data_manager):
    st.header("Student Stats Overview")

    if data_manager.students_df.empty:
        st.info("No students registered yet. Add students through the Student Management panel.")
        return

    # Create a grid layout for student boxes
    cols_per_row = 3
    students = data_manager.students_df.to_dict('records')

    # Custom CSS for student boxes
    st.markdown("""
    <style>
    .student-box {
        background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
        border: 2px solid #00ff9f;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.2);
    }
    .stat-value {
        color: #00ff9f;
        font-family: monospace;
        font-size: 1.2em;
    }
    .student-name {
        color: #ffffff;
        font-family: monospace;
        font-size: 1.4em;
        text-shadow: 0 0 10px #00ff9f;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create rows of students
    for i in range(0, len(students), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(students):
                student = students[i + j]
                with col:
                    st.markdown(f"""
                    <div class="student-box">
                        <div class="student-name">{student['name']}</div>
                        <hr style="border-color: #00ff9f; margin: 10px 0;">
                        <div>XP: <span class="stat-value">{student['xp']}</span></div>
                        <div>Gold: <span class="stat-value">{student['gold']}</span></div>
                        <div>HP: <span class="stat-value">{student['hp']}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

def display_leaderboard(data_manager):
    display_student_stats(data_manager)