from pydantic import BaseModel

from .classroom import Classroom


class Curriculum(BaseModel):
    teachers: int
    course_key: str
    grade: str
    session_length: int
    session: int
    week: int
    classroom: Classroom


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
