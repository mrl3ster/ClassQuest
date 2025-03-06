import streamlit as st
from utils.constants import BADGE_IMAGES
from components.card_system import create_privilege_card

def teacher_dashboard(data_manager):
    st.title("Teacher Dashboard")

    tab1, tab2, tab3 = st.tabs(["Student Management", "Stats Management", "Privilege Cards"])

    with tab1:
        st.subheader("Add New Student")
        new_student = st.text_input("Student Name")
        student_password = st.text_input("Student Password", type="password")
        if st.button("Add Student"):
            if new_student and student_password:
                if data_manager.add_student(new_student, student_password):
                    st.success(f"Added student: {new_student}")
                else:
                    st.error("Student already exists!")
            else:
                st.error("Please provide both name and password")

    with tab2:
        st.subheader("Manage Student Stats")
        student = st.selectbox("Select Student", data_manager.students_df['name'].tolist())

        if student:
            stats = data_manager.get_student_stats(student)

            # Custom CSS for stat management
            st.markdown("""
            <style>
            .stat-container {
                background: linear-gradient(45deg, #1a1f4c, #0a0f2c);
                border: 2px solid #00ff9f;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }
            .stat-value {
                color: #00ff9f;
                font-family: monospace;
                font-size: 1.2em;
            }
            </style>
            """, unsafe_allow_html=True)

            # Gold Management
            st.markdown('<div class="stat-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("-10 Gold", key="gold_minus"):
                    new_gold = max(0, stats['gold'] - 10)
                    data_manager.update_student_stats(student, 'gold', new_gold)
                    st.rerun()
            with col2:
                st.markdown(f'<div style="text-align: center">Gold: <span class="stat-value">{stats["gold"]}</span></div>', unsafe_allow_html=True)
            with col3:
                if st.button("+10 Gold", key="gold_plus"):
                    new_gold = stats['gold'] + 10
                    data_manager.update_student_stats(student, 'gold', new_gold)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            # XP Management
            st.markdown('<div class="stat-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("-50 XP", key="xp_minus"):
                    new_xp = max(0, stats['xp'] - 50)
                    data_manager.update_student_stats(student, 'xp', new_xp)
                    st.rerun()
            with col2:
                st.markdown(f'<div style="text-align: center">XP: <span class="stat-value">{stats["xp"]}</span></div>', unsafe_allow_html=True)
            with col3:
                if st.button("+50 XP", key="xp_plus"):
                    new_xp = stats['xp'] + 50
                    data_manager.update_student_stats(student, 'xp', new_xp)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            # HP Management
            st.markdown('<div class="stat-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("-5 HP", key="hp_minus"):
                    new_hp = max(0, stats['hp'] - 5)
                    data_manager.update_student_stats(student, 'hp', new_hp)
                    st.rerun()
            with col2:
                st.markdown(f'<div style="text-align: center">HP: <span class="stat-value">{stats["hp"]}</span></div>', unsafe_allow_html=True)
            with col3:
                if st.button("+5 HP", key="hp_plus"):
                    new_hp = min(100, stats['hp'] + 5)
                    data_manager.update_student_stats(student, 'hp', new_hp)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        create_privilege_card(data_manager)

def award_badge(data_manager, student_name):
    st.subheader("Award Achievement Badge")

    cols = st.columns(5)
    for idx, badge_url in enumerate(BADGE_IMAGES):
        with cols[idx]:
            st.image(badge_url, caption=f"Badge {idx+1}")
            if st.button(f"Award Badge {idx+1}", key=f"badge_{idx}"):
                student_data = data_manager.get_student_stats(student_name)
                if student_data:
                    data_manager.update_student_stats(student_name, 'xp', student_data['xp'] + 100)
                    st.success(f"Awarded Badge {idx+1} to {student_name}!")