import streamlit as st
from utils.constants import AVATAR_IMAGES

def customize_profile(data_manager, student_name):
    st.header("Customize Your Profile")

    student_data = data_manager.get_student_stats(student_name)
    if not student_data:
        return

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

    # Display current avatar
    st.markdown("""
    <div class="student-box">
        <div class="student-name">Current Symbol</div>
        <hr style="border-color: #00ff9f; margin: 10px 0;">
    """, unsafe_allow_html=True)
    st.markdown(student_data['avatar_url'], unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Avatar selection
    st.subheader("Choose Your Symbol")

    cols = st.columns(5)
    for idx, avatar_svg in enumerate(AVATAR_IMAGES):
        with cols[idx]:
            st.markdown("""
            <div class="student-box" style="text-align: center;">
            """, unsafe_allow_html=True)
            st.markdown(avatar_svg, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button(f"Select Symbol {idx + 1}", key=f"avatar_{idx}"):
                data_manager.update_student_stats(student_name, 'avatar_url', avatar_svg)
                st.success("Symbol updated!")
                st.rerun()