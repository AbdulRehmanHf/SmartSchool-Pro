# services/student_manager.py
import json
import os
from typing import List, Optional
from models.student import Student

DATA_FILE = "data/students.json"

class StudentManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.students: List[Student] = self._load_students()
        self.next_id = self._calculate_next_id()  # ← Short ID ke liye

    def _calculate_next_id(self) -> int:
        """Existing students mein se sabse bada number dhundega aur +1 karega"""
        if not self.students:
            return 1
        max_num = 0
        for student in self.students:
            if student.id.startswith("STU-"):
                try:
                    num = int(student.id.split("-")[1])
                    if num > max_num:
                        max_num = num
                except:
                    continue
        return max_num + 1

    def _load_students(self) -> List[Student]:
        if not os.path.exists(DATA_FILE):
            return self._create_sample_data()
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                students = [Student.from_dict(s) for s in data]
                return students
        except Exception as e:
            print(f"Error loading data: {e}")
            return self._create_sample_data()

    def _save_students(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=2)

    def _create_sample_data(self) -> List[Student]:
        sample = [
            Student("STU-001", "Alice Johnson", 16, "10th", "alice@school.com", "+1234567890", 92.5),
            Student("STU-002", "Bob Smith", 17, "11th", "bob@school.com", "+1234567891", 78.0),
            Student("STU-003", "Emma Wilson", 15, "9th", "emma@school.com", "+1234567892", 88.7),
        ]
        self.students = sample
        self.next_id = 4  # Agla ID STU-004 hoga
        self._save_students()
        return sample[:]

    def get_all(self) -> List[Student]:
        return self.students

    def add(self, student: Student):
        student.id = f"STU-{self.next_id:03d}"  # ← Beautiful short ID!
        self.students.append(student)
        self.next_id += 1
        self._save_students()

    def update(self, student_id: str, updated_student: Student) -> bool:
        for i, s in enumerate(self.students):
            if s.id == student_id:
                updated_student.id = student_id  # ID change nahi hogi
                self.students[i] = updated_student
                self._save_students()
                return True
        return False

    def delete(self, student_id: str) -> bool:
        for i, s in enumerate(self.students):
            if s.id == student_id:
                self.students.pop(i)
                self._save_students()
                return True
        return False

    def get_by_id(self, student_id: str) -> Optional[Student]:
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    def search(self, query: str) -> List[Student]:
        query = query.lower()
        return [s for s in self.students if query in s.name.lower() or query in s.email.lower()]