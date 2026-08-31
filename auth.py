import hashlib
import streamlit as st
import database

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_auth_state():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

def login(username_or_email: str, password: str) -> tuple[bool, str]:
    pwd_hash = hash_password(password)
    user = database.verify_user_credentials(username_or_email, pwd_hash)
    if user:
        st.session_state.user = user
        st.session_state.authenticated = True
        return True, "Login successful!"
    return False, "Invalid username/email or password."

def logout():
    st.session_state.user = None
    st.session_state.authenticated = False
    st.rerun()

def get_current_user():
    return st.session_state.get("user")

def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)

