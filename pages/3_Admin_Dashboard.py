# pages/3_Admin_Dashboard.py
import streamlit as st
from utils.db import users
import bcrypt
from utils.auth import auth
import time


st.set_page_config(page_title="Admin Dashboard", layout="wide")

auth()

# Hide "app" from sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] li:first-child {
            display: none;
        }
    </style>
""",
    unsafe_allow_html=True,
)

if st.session_state.authenticated and st.session_state.user_role == "admin":
    st.title("Admin Dashboard")
    

    # Create tabs for different admin functions
    tab1, tab2, tab3 = st.tabs(["Create User", "Manage Users", "Delete Users"])

    with tab1:
        st.header("Create New User")
        with st.form("create_user_form"):
            new_name = st.text_input("Name")
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_role = st.selectbox("Role", ["user", "admin"])

            submit = st.form_submit_button("Create User")

            if submit:
                if not new_username or not new_email or not new_password or not new_name:
                    st.error("All fields are required!")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                elif users.find_one({"username": new_username}):
                    st.error("Username already exists!")
                elif users.find_one({"email": new_email}):
                    st.error("Email already registered!")
                else:
                    # Hash the password
                    hashed_password = bcrypt.hashpw(
                        new_password.encode("utf-8"), bcrypt.gensalt()
                    )

                    # Create new user document
                    new_user = {
                        "username": new_username,
                        "email": new_email,
                        "password": hashed_password.decode("utf-8"),
                        "role": new_role,
                        "name": new_name
                    }

                    # Insert into database
                    users.insert_one(new_user)
                    st.success(f"User {new_username} created successfully!")
                    time.sleep(2)
                    st.rerun()

    with tab2:
        st.header("User Management")

        # Display all users
        user_list = list(users.find({}, {"password": 0}))

        # Create a DataFrame for better display
        import pandas as pd

        df = pd.DataFrame(user_list)
        if not df.empty:
            df = df.drop("_id", axis=1)
            st.dataframe(df, hide_index=True)

        # User Role Management
        st.subheader("Modify User Role")
        col1, col2 = st.columns(2)
        with col1:
            selected_user = st.selectbox(
                "Select User", [user["username"] for user in user_list]
            )
        with col2:
            new_role = st.selectbox("New Role", ["user", "admin"])

        if st.button("Update Role"):
            users.update_one({"username": selected_user}, {"$set": {"role": new_role}})
            st.success(f"Updated role for {selected_user} to {new_role}")
            st.rerun()

    with tab3:
        st.header("Delete User")
        user_to_delete = st.selectbox(
            "Select User to Delete", [user["username"] for user in user_list]
        )

        if st.button("Delete User", type="primary"):
            if user_to_delete == st.session_state.username:
                st.error("You cannot delete your own account!")
            else:
                users.delete_one({"username": user_to_delete})
                st.success(f"Deleted user {user_to_delete}")
                st.rerun()

else:
    st.warning("You don't have permission to access this page.")
