# app.py
import streamlit as st
import bcrypt
from utils.db import users


def login_user(username, password):
    user = users.find_one({"username": username})
    if user and bcrypt.checkpw(
        password.encode("utf-8"), user["password"].encode("utf-8")
    ):
        st.session_state.authenticated = True
        st.session_state.user_role = user["role"]
        st.session_state.username = username
        st.session_state.user = user
        return True
    return False


def register_user(username, password, email):
    if users.find_one({"username": username}):
        return False, "Username already exists"
    if users.find_one({"email": email}):
        return False, "Email already registered"

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {
        "username": username,
        "password": hashed_password.decode("utf-8"),
        "email": email,
        "role": "user",
    }
    users.insert_one(user)
    return True, "Registration successful"


def auth():
    # Initialize session states
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "username" not in st.session_state:
        st.session_state.username = None

    # Sidebar login/register system
    with st.sidebar:
        if not st.session_state.authenticated:
            st.title("Authentication")
            tab1, tab2 = st.tabs(["Login", "Register"])

            with tab1:
                st.subheader("Login")
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input(
                    "Password", type="password", key="login_password"
                )

                if st.button("Login"):
                    if login_user(login_username, login_password):
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

            with tab2:
                st.subheader("Register")
                reg_username = st.text_input("Username", key="reg_username")
                reg_email = st.text_input("Email", key="reg_email")
                reg_password = st.text_input(
                    "Password", type="password", key="reg_password"
                )
                reg_confirm_password = st.text_input(
                    "Confirm Password", type="password", key="reg_confirm_password"
                )

                if st.button("Register"):
                    if reg_password != reg_confirm_password:
                        st.error("Passwords do not match")
                    elif len(reg_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, message = register_user(
                            reg_username, reg_password, reg_email
                        )
                        if success:
                            st.success(message)
                            st.info("Please login with your credentials")
                        else:
                            st.error(message)

        else:
            name = st.session_state.user["name"]
            role = st.session_state.user_role
            st.title(f"Welcome, {name}!")
            st.write(f"Role: {role}")
            if st.button("Logout"):
                st.session_state.user = None
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.rerun()
