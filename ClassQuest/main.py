import streamlit as st
from utils.authentication import initialize_auth, login, logout
from data_manager import DataManager
from components.teacher_dashboard import teacher_dashboard
from components.student_view import student_view
from components.leaderboard import display_leaderboard
from components.card_system import display_card_shop, display_student_cards

# Page config
st.set_page_config(
    page_title="ClassQuest",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize authentication
initialize_auth()

# Initialize data manager
data_manager = DataManager()

# Main app logic
if not st.session_state.authenticated:
    login()
else:
    # Header with welcome message and logout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("ClassQuest")
        st.write(f"Welcome, {st.session_state.username}!")
    with col2:
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

    # Main content
    if st.session_state.user_type == "teacher":
        teacher_dashboard(data_manager)
        st.markdown("---")
        display_leaderboard(data_manager)
    else:  # student view
        student_view(data_manager, st.session_state.username)
        st.markdown("---")
        display_leaderboard(data_manager)