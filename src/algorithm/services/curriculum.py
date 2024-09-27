import json

from src.algorithm.models.classroom import Classroom
from src.algorithm.models.curriculum import Curriculum, SchoolCurriculum
from src.algorithm.services.school_curriculum import SchoolCurriculumService

school_curriculum_service = SchoolCurriculumService()

SESSION_LIST = [
    "1",
    "2",
    "3",
    "4",
    "20",
    "5",
    "6",
    "7",
    "8",
    "9",
    # "30",
    "40",
    "50",
    "60",
    "70",
]


class CurriculumService:
    def __init__(self):
        self.curriculum_repository = "data/course/course_washed.json"
        self.school_curriculums = school_curriculum_service.get_school_curriculums()

    def convert_to_school_curriculum(
        self, curriculums: list[Curriculum]
    ) -> list[SchoolCurriculum]:
        school_curriculums = []

        for curriculum in curriculums:
            SCHOOL_CURRUCULUM_TEMPLATE: SchoolCurriculum = list(
                filter(
                    lambda x: x.course_id + x.class_id == curriculum.course_key,
                    self.school_curriculums,
                )
            )[0]

            course_id, class_id = curriculum.course_key[:5], curriculum.course_key[5:]
            course_name = SCHOOL_CURRUCULUM_TEMPLATE.course_name
            course_type = SCHOOL_CURRUCULUM_TEMPLATE.course_type
            session_length = curriculum.session_length
            teacher_list = school_curriculum_service.get_teacher_by_id(
                curriculum.teachers
            )
            week = int(curriculum.week)
            session = str(curriculum.session)
            classroom = curriculum.classroom.id

            school_curriculums.append(
                SchoolCurriculum(
                    course_id=course_id,
                    course_name=course_name,
                    course_type=course_type,
                    class_id=class_id,
                    session_length=session_length,
                    teacher_list=teacher_list,
                    week=week,
                    session=session,
                    classroom=classroom,
                )
            )

        result_chromosome = []

        for chromosome in school_curriculums:
            session = chromosome.session  # chromosome["session"]
            session_idx = SESSION_LIST.index(session)

            for i in range(chromosome.session_length):
                chromosome.session = SESSION_LIST[(session_idx + i) % len(SESSION_LIST)]
                # if 5 <= session_idx + i and session_idx + i <= 9:
                #     chromosome.session = "0" + chromosome.session
                result_chromosome.append(chromosome.copy())

        return result_chromosome


# service = CurriculumService()
