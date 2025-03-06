import streamlit as st
import pandas as pd

def initialize_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'username' not in st.session_state:
        st.session_state.username = None

def login():
    st.title("ClassQuest")
    st.markdown("""
    <style>
    .stTitle {
        font-family: monospace;
        text-shadow: 0 0 10px #00ff9f, 0 0 20px #00ff9f, 0 0 30px #00ff9f;
        color: #00ff9f;
    }

    /* Star background */
    body {
        background: radial-gradient(ellipse at bottom, #0a0f2c 0%, #090a0f 100%);
        overflow: hidden;
    }

    /* Shooting stars animation */
    .shooting-star {
        position: fixed;
        top: 50%;
        left: 50%;
        width: 4px;
        height: 4px;
        background: #fff;
        border-radius: 50%;
        box-shadow: 0 0 0 4px rgba(255,255,255,0.1),
                    0 0 0 8px rgba(255,255,255,0.1),
                    0 0 20px rgba(255,255,255,1);
        animation: shoot 3s linear infinite;
    }

    .shooting-star::before {
        content: '';
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 300px;
        height: 1px;
        background: linear-gradient(90deg, #fff, transparent);
    }

    @keyframes shoot {
        0% {
            transform: rotate(315deg) translateX(0);
            opacity: 1;
        }
        70% {
            opacity: 1;
        }
        100% {
            transform: rotate(315deg) translateX(-1000px);
            opacity: 0;
        }
    }

    /* Multiple shooting stars with different delays */
    .shooting-star:nth-child(1) { animation-delay: 0s; top: 0%; }
    .shooting-star:nth-child(2) { animation-delay: 1.2s; top: 20%; }
    .shooting-star:nth-child(3) { animation-delay: 2.4s; top: 40%; }
    .shooting-star:nth-child(4) { animation-delay: 3.6s; top: 60%; }
    .shooting-star:nth-child(5) { animation-delay: 4.8s; top: 80%; }

    .stButton>button {
        background-color: #00ff9f;
        color: #0a0f2c;
        border: 2px solid #00ff9f;
        border-radius: 5px;
        box-shadow: 0 0 10px #00ff9f;
        font-family: monospace;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: transparent;
        color: #00ff9f;
        box-shadow: 0 0 20px #00ff9f;
    }
    .stSelectbox, .stTextInput {
        background-color: #1a1f4c;
        border: 1px solid #00ff9f;
        border-radius: 5px;
        color: #ffffff;
    }
    </style>

    <!-- Shooting stars elements -->
    <div class="shooting-star"></div>
    <div class="shooting-star"></div>
    <div class="shooting-star"></div>
    <div class="shooting-star"></div>
    <div class="shooting-star"></div>
    """, unsafe_allow_html=True)

    st.markdown("### Enter the Learning Galaxy")

    login_type = st.selectbox("Select Your Role", ["Teacher", "Student"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Launch Mission"):
        if login_type == "Teacher" and password == "teacher123":  # Simple password for demo
            st.session_state.authenticated = True
            st.session_state.user_type = "teacher"
            st.session_state.username = username
            st.success("Welcome, Mission Commander")
            st.rerun()
        elif login_type == "Student":
            from data_manager import DataManager
            data_manager = DataManager()
            if data_manager.verify_student_password(username, password):
                st.session_state.authenticated = True
                st.session_state.user_type = "student"
                st.session_state.username = username
                st.success("Cadet Login Successful")
                st.rerun()
            else:
                st.error("Invalid credentials")
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.username = None