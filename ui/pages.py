# ui/pages.py ← Pura file isi se replace kar do (100% FINAL & WORKING)

import streamlit as st
import re
import uuid
import pandas as pd
import os
from models.student import Student
from services.student_manager import StudentManager


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    pattern = r"^\+?\d[\d \-\(\)]{9,14}$"
    return re.match(pattern, phone) is not None


def show_students_page():
    if 'manager' not in st.session_state:
        st.session_state.manager = StudentManager()

    manager = st.session_state.manager

    st.title("SmartSchool Pro v2.0")
    st.markdown("**Professional Student Management System • Made with ❤️**")

    menu = [
        "Dashboard",
        "Add Student",
        "View All Students",
        "Update Student",
        "Delete Student",
        "Search & Filter",
        "Statistics"
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    # ==================== DASHBOARD ====================
    if choice == "Dashboard":
        st.header("Dashboard Overview")
        students = manager.get_all()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", len(students))
        with col2:
            avg_age = round(sum(s.age for s in students)/len(students), 1) if students else 0
            st.metric("Average Age", avg_age)
        with col3:
            avg_score = round(sum(s.performance_score for s in students)/len(students), 1) if students else 0
            st.metric("Avg Performance", f"{avg_score}%")
        with col4:
            top = max(students, key=lambda x: x.performance_score, default=None)
            st.metric("Top Performer", top.name if top else "N/A")

        st.markdown("### Top 5 Performers Leaderboard")
        if students:
            top5 = sorted(students, key=lambda x: x.performance_score, reverse=True)[:5]
            for i, s in enumerate(top5):
                medal = "1st" if i == 0 else "2nd" if i == 1 else "3rd" if i == 2 else f"{i+1}th"
                st.markdown(f"**{medal} {s.name}** → {s.performance_score}% (Grade {s.grade})")
        else:
            st.info("No students yet")

        st.markdown("### Export Data")
        if students:
            df = pd.DataFrame([s.to_dict() for s in students])
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Complete Report (CSV)",
                data=csv,
                file_name="SmartSchool_Students_Report.csv",
                mime="text/csv",
                use_container_width=True
            )

    # ==================== ADD STUDENT WITH PHOTO ====================
    elif choice == "Add Student":
        st.header("Add New Student")
        with st.form("add_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*", placeholder="Ahmed Khan")
                age = st.number_input("Age*", 10, 25, 16)
                grade = st.selectbox("Grade*", ["9th", "10th", "11th", "12th"])
            with col2:
                email = st.text_input("Email*", placeholder="ahmed@example.com")
                phone = st.text_input("Phone*", placeholder="+923001234567")
                score = st.slider("Performance Score (%)", 0.0, 100.0, 85.0, 0.5)

            uploaded_photo = st.file_uploader("Upload Student Photo (JPG/PNG)", type=["jpg", "jpeg", "png"])

            submitted = st.form_submit_button("Add Student", use_container_width=True)

            if submitted:
                if not all([name, email, phone]):
                    st.error("Please fill all required fields!")
                elif not validate_email(email):
                    st.error("Invalid email format")
                elif not validate_phone(phone):
                    st.error("Invalid phone number")
                else:
                    new_student = Student("", name.strip(), int(age), grade, email.strip(), phone.strip(), float(score))
                    manager.add(new_student)

                    if uploaded_photo:
                        try:
                            os.makedirs("photos", exist_ok=True)
                            with open(f"photos/{new_student.id}.jpg", "wb") as f:
                                f.write(uploaded_photo.getvalue())
                            st.image(uploaded_photo, caption="Photo saved!", width=200)
                        except:
                            st.warning("Photo issue, but student added.")
                    
                    st.success(f"{name} (ID: {new_student.id}) added!")
                    st.balloons()

    # ==================== VIEW ALL STUDENTS - PHOTO GALLERY ====================
        # ==================== VIEW ALL STUDENTS - PERFECT GALLERY (NAAM CENTER + BEAUTIFUL) ====================
    elif choice == "View All Students":
        st.header("Student Photo Gallery")

        students = manager.get_all()
        if not students:
            st.info("No students added yet")
            return

        # 4 columns banao
        cols = st.columns(4)
        
        for i, s in enumerate(students):
            with cols[i % 4]:
                # Card style box banao taake sab equal dikhe
                with st.container():
                    # Center everything
                    st.markdown(
                        f"""
                        <div style="text-align: center; padding: 15px; border: 2px solid #d0d0d0; border-radius: 15px; margin: 10px 0; background-color: #f9f9f9;">
                            <h3 style="margin: 0; color: #1e3799;">{s.name}</h3>
                            <p style="margin: 5px 0; font-size: 14px; color: #666;">
                                <strong>ID:</strong> {s.id}<br>
                                <strong>Grade:</strong> {s.grade} | <strong>Score:</strong> {s.performance_score}%
                            </p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

                    # Photo section - fixed height taake alignment disturb na ho
                    photo_path = f"photos/{s.id}.jpg"
                    if os.path.exists(photo_path):
                        try:
                            st.image(photo_path, use_container_width=True)
                        except:
                            st.image("https://via.placeholder.com/300x300.png?text=Error+Photo", use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x300.png?text=No+Photo", use_container_width=True)
                    
                    # Bottom line
                    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
                    
    # ==================== UPDATE STUDENT - 100% WORKING ====================
    elif choice == "Update Student":
        st.header("Update Student Information")
        students = manager.get_all()
        if not students:
            st.info("No students to update")
        else:
            options = {f"{s.name} ({s.id}) - Grade {s.grade}": s for s in students}
            selected = st.selectbox("Select Student", list(options.keys()))
            student = options[selected]

            # Show current photo
            photo_path = f"photos/{student.id}.jpg"
            if os.path.exists(photo_path):
                try:
                    st.image(photo_path, caption="Current Photo", width=250)
                except:
                    st.warning("Photo corrupted")

            with st.form("update_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Name", value=student.name)
                    age = st.number_input("Age", 10, 25, value=student.age)
                    grade = st.selectbox("Grade", ["9th","10th","11th","12th"], index=["9th","10th","11th","12th"].index(student.grade))
                with col2:
                    email = st.text_input("Email", value=student.email)
                    phone = st.text_input("Phone", value=student.phone)
                    score = st.slider("Performance Score", 0.0, 100.0, student.performance_score)

                new_photo = st.file_uploader("Upload New Photo (Optional)", type=["jpg", "jpeg", "png"])

                if st.form_submit_button("Update Student", use_container_width=True):
                    if validate_email(email) and validate_phone(phone):
                        updated = Student(student.id, name, age, grade, email, phone, score)
                        manager.update(student.id, updated)

                        if new_photo:
                            try:
                                with open(photo_path, "wb") as f:
                                    f.write(new_photo.getvalue())
                                st.success("Photo updated!")
                            except:
                                st.error("Photo failed")

                        st.success("Student updated successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Invalid email or phone")

    # ==================== DELETE STUDENT ====================
    elif choice == "Delete Student":
        st.header("Delete Student")
        students = manager.get_all()
        if students:
            options = {f"{s.name} ({s.id})": s for s in students}
            selected = st.selectbox("Select to delete", options.keys())
            student = options[selected]
            st.warning(f"Delete **{student.name}** permanently?")
            if st.button("Yes, Delete Forever", type="primary"):
                manager.delete(student.id)
                photo_path = f"photos/{student.id}.jpg"
                if os.path.exists(photo_path):
                    os.remove(photo_path)
                st.success("Deleted!")
                st.balloons()
                st.rerun()

    # ==================== SEARCH & STATISTICS ====================
    elif choice == "Search & Filter":
        st.header("Search Students")
        search = st.text_input("Search by name/email")
        results = [s for s in manager.get_all() if search.lower() in s.name.lower() or search.lower() in s.email.lower()]
        for s in results:
            st.write(f"**{s.name}** - {s.id} - {s.grade} - {s.performance_score}%")

    elif choice == "Statistics":
        st.header("Analytics")
        students = manager.get_all()
        if students:
            df = pd.DataFrame([s.to_dict() for s in students])
            st.bar_chart(df.groupby("grade")["performance_score"].mean())
            st.line_chart(df["age"].value_counts().sort_index())