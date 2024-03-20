import json
from itertools import chain

from src.algorithm.models.classroom import Classroom
from src.algorithm.models.curriculum import Curriculum, SchoolCurriculum


class SchoolCurriculumService:
    instance = None

    def __init__(self):
        self.curriculum_repository = "data/course/course_washed.json"
        self.teacher_id_table = {}
        self.id_teacher_table = {}
        self._school_curriculums = self.get_school_curriculums()
        self._classrooms = self.all_classrooms()
        self._teachers = self.all_teachers()
        self._course_keys = self.all_course_keys()

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_school_curriculums(self) -> list[SchoolCurriculum]:
        with open(self.curriculum_repository, "r") as f:
            data = json.load(f)
        school_curriculums = [
            SchoolCurriculum(
                course_id=curriculum["course_id"],
                course_name=curriculum["course_name"],
                course_type=curriculum["course_type"],
                class_id=curriculum["class_id"],
                session=curriculum["session"],
                session_length=curriculum["session_length"],
                teacher_list=curriculum["teacher_list"],
                week=int(curriculum["week"]),
                classroom=curriculum["classroom"],
            )
            for curriculum in data
        ]
        return school_curriculums

    def convert_to_curriculum(
        self, school_curriculums: list[SchoolCurriculum]
    ) -> list[Curriculum]:
        curriculums = []
        for school_curriculum in school_curriculums:
            course_key = school_curriculum.course_id + school_curriculum.class_id
            teachers = self.get_teacher_id(school_curriculum.teacher_list)
            classroom = Classroom(id=school_curriculum.classroom, size=None, type=None)
            curriculum = Curriculum(
                teachers=teachers,
                course_key=course_key,
                grade=school_curriculum.class_id[-3],
                session=school_curriculum.session,
                session_length=school_curriculum.session_length,
                week=int(school_curriculum.week),
                classroom=classroom,
            )
            curriculums.append(curriculum)
        return curriculums

    def all_course_keys(self) -> list[str]:
        return [
            str(curriculum.course_id) + str(curriculum.class_id)
            for curriculum in self.school_curriculums
        ]

    def all_classrooms(self) -> list[Classroom]:
        classrooms = list(
            [
                curriculum.classroom if curriculum.classroom else "班會"
                for curriculum in self.school_curriculums
            ]
        )
        # TODO: Add classroom size and type
        classrooms = [
            Classroom(id=classroom, size=None, type=None) for classroom in classrooms
        ]
        return classrooms

    def get_teacher_by_id(self, teacher_id: int) -> list[str]:
        return self.id_teacher_table[teacher_id].split(", ")

    def get_teacher_id(self, teacher_name: str | list[str]) -> int:
        if isinstance(teacher_name, list):
            teacher_name = ", ".join(teacher_name)
        if teacher_name not in self.teacher_id_table:
            teacher_id = len(self.teacher_id_table)
            self.teacher_id_table[teacher_name] = teacher_id
            self.id_teacher_table[teacher_id] = teacher_name
        return self.teacher_id_table[teacher_name]

    def all_teachers(self) -> list[int]:
        teachers = []
        for curriculum in self.school_curriculums:
            teacher_name = ", ".join(curriculum.teacher_list)
            if teacher_name in self.teacher_id_table:
                teachers.append(self.teacher_id_table[teacher_name])
            else:
                teacher_id = len(self.teacher_id_table)
                self.teacher_id_table[teacher_name] = teacher_id
                self.id_teacher_table[teacher_id] = teacher_name
                teachers.append(teacher_id)
        return teachers

    @property
    def school_curriculums(self) -> list[SchoolCurriculum]:
        return self._school_curriculums

    @property
    def classrooms(self) -> list[Classroom]:
        return self._classrooms

    @property
    def teachers(self) -> list[str]:
        return self._teachers

    @property
    def course_keys(self) -> list[str]:
        return self._course_keys


# service = SchoolCurriculumService()
# print(service.convert_to_curriculum(service.school_curriculums))
