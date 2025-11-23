from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class Student:
    id: str
    name: str
    age: int
    grade: str
    email: str
    phone: str
    performance_score: float  # 0.0 - 100.0

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "email": self.email,
            "phone": self.phone,
            "performance_score": self.performance_score
        }

    @staticmethod
    def from_dict(data: dict) -> 'Student':
        return Student(
            id=data.get("id", str(uuid.uuid4())),
            name=data["name"],
            age=data["age"],
            grade=data["grade"],
            email=data["email"],
            phone=data["phone"],
            performance_score=data["performance_score"]
        )