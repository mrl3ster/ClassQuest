import streamlit as st
import plotly.express as px
from components.card_system import display_student_cards, display_card_shop
from components.profile_customization import customize_profile

def student_view(data_manager, student_name):
    st.title(f"Welcome, {student_name}")

    # Display student stats
    stats = data_manager.get_student_stats(student_name)
    if stats:
        # Display current avatar and stats
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(stats['avatar_url'], unsafe_allow_html=True)
            if st.button("Choose Your Symbol"):
                st.session_state.active_tab = "Profile"
                st.rerun()
        with col2:
            stat_cols = st.columns(4)
            with stat_cols[0]:
                st.metric("Level", stats['level'])
            with stat_cols[1]:
                st.metric("Gold", stats['gold'])
            with stat_cols[2]:
                st.metric("XP", stats['xp'])
            with stat_cols[3]:
                st.metric("HP", stats['hp'])

        # Initialize session state for active tab if not exists
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = "My Cards"

        # Tabs for different sections
        tab1, tab2, tab3 = st.tabs(["Profile", "My Cards", "Card Shop"])

        # Show the appropriate tab based on session state
        if st.session_state.active_tab == "Profile":
            with tab1:
                customize_profile(data_manager, student_name)
            st.session_state.active_tab = None  # Reset after showing
        with tab2:
            display_student_cards(data_manager, student_name)
        with tab3:
            display_card_shop(data_manager, student_name)