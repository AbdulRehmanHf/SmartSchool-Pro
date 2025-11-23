# main.py  ← Pura file isi se replace kar do

import streamlit as st
from ui.pages import show_students_page

# ===== LOGIN SYSTEM (Sir ko yeh dekh ke rona aa jayega) =====
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.image("https://www.icevonline.com/wp-content/uploads/2020/08/school-logo.png", width=200)  # Optional logo
    st.title("🔐 SmartSchool Pro v2.0")
    st.markdown("### Admin Login Panel")
    
    password = st.text_input("Enter Password", type="password")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🚪 Login", use_container_width=True):
            if password == "12345":        # ← Yahan apna password daal do (jaise admin, sir123, etc.)
                st.session_state.logged_in = True
                st.success("✅ Login Successful!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Wrong password! Try again.")
    with col2:
        st.write("**Hint:** Password is `12345`")  # Sir ko bata do ya hata do
else:
    # Login ho gaya to pura app dikhao
    st.set_page_config(page_title="SmartSchool Pro", page_icon="🏫", layout="wide")
    show_students_page()