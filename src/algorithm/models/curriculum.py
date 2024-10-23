from pydantic import BaseModel
from typing import Optional

from .classroom import Classroom


class Curriculum(BaseModel):
    teachers: int
    course_key: str
    course_type: str
    grade: str
    course_class: str
    session_length: int
    session: int
    week: int
    classroom: Classroom
    class_size: int
    class_type: str


class SchoolCurriculum(BaseModel):
    course_id: str
    course_name: str
    course_type: str
    class_id: str
    session: str
    session_length: int
    teacher_list: list[str]
    week: int
    classroom: str
    class_size: int
    class_type: str
    grade: Optional[int] = -1
