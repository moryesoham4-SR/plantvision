import hashlib
import streamlit as st
import database

def hash_password(password: str) -> str:
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()

def init_auth_state():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

def login(username_or_email: str, password: str) -> tuple[bool, str]:
    if not username_or_email or not password:
        return False, "Please enter both username/email and password."
    success, user, msg = database.verify_user_credentials(username_or_email, password)
    if success and user:
        set_user_session(user)
        return True, msg
    return False, msg



def set_user_session(user: dict):
    st.session_state.user = user
    st.session_state.authenticated = True

def login_by_id(user_id: int) -> bool:
    user = database.get_user_by_id(user_id)
    if user:
        set_user_session(user)
        return True
    return False

def logout():
    st.session_state.user = None
    st.session_state.authenticated = False
    st.rerun()

def get_current_user():
    return st.session_state.get("user")

def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


