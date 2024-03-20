import json
import random

from src.algorithm.models.curriculum import Curriculum, SchoolCurriculum
from src.algorithm.services.school_curriculum import SchoolCurriculumService

school_curriculum_service = SchoolCurriculumService()


def test_school_curriculum_instance():
    another_school_curriculum_service = SchoolCurriculumService()
    assert school_curriculum_service is another_school_curriculum_service


def test_school_curriculum_get_school_curriculums():
    curriculum_data = "data/course/course_washed.json"
    with open(curriculum_data, "r") as f:
        data = json.load(f)
        assert len(data) == len(school_curriculum_service.school_curriculums)

    school_curriculums = [
        SchoolCurriculum(
            course_id=curriculum["course_id"],
            course_name=curriculum["course_name"],
            course_type=curriculum["course_type"],
            class_id=curriculum["class_id"],
            session_length=curriculum["session_length"],
            teacher_list=curriculum["teacher_list"],
            week=curriculum["week"],
            classroom=curriculum["classroom"],
        )
        for curriculum in data
    ]

    choosen_curriculums = random.choices(school_curriculums, k=10)

    for curriculum in choosen_curriculums:
        assert curriculum in school_curriculum_service.school_curriculums


def test_school_curriculum_len():
    assert len(school_curriculum_service.course_keys) == len(
        school_curriculum_service.teachers
    )
    assert len(school_curriculum_service.course_keys) == len(
        school_curriculum_service.classrooms
    )
    assert len(school_curriculum_service.course_keys) == len(
        school_curriculum_service.school_curriculums
    )
