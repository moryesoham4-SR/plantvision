import hashlib
import streamlit as st
import database

def hash_password(password: str) -> str:
    # SHA-256 with fixed application salt
    salt = plantvision_ai_secure_salt_2026
    return hashlib.sha256((password + salt).encode(utf-8)).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def init_auth_state():
    if authenticated not in st.session_state:
        st.session_state.authenticated = False
    if user not in st.session_state:
        st.session_state.user = None

def login(username, password):
    user = database.get_user_by_username(username)
    if user and verify_password(password, user[password_hash]):
        st.session_state.authenticated = True
        st.session_state.user = {
            id: user[id],
            username: user[username],
            full_name: user[full_name],
            email: user[email],
            created_at: user[created_at]
        }
        return True, Login successful!
    return False, Invalid username or password.

def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

def get_current_user():
    return st.session_state.get(user, None)

def is_authenticated():
    return st.session_state.get(authenticated, False)
