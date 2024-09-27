from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]
@FitnessRegistry.register("ConflictGradeCourse", weight=-1000)
class ConflictGradeCourse(FitnessBase):
    name = "ConflictGradeCourse"
    show_name = "衝同年級必選修"
    description = "If the same grade has the same course, the fitness will be added by 1000."

    @staticmethod
    def combine_session_week(session, week):
        return str(session) + str(week)

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        # class_session_dict = {}
        # elective_grade_course_dict = {str(_) : {} for _ in range(1, 7)}
        # compulsory_grade_course_dict = {str(_) : {} for _ in range(1, 7)}
        # course_type_grade_course_dict = {
        #     "選修": {str(_) : {} for _ in range(1, 7)},
        #     "必修": {str(_) : {} for _ in range(1, 7)}
        # }

        course_type_grade_course_dict = {
            str(_) : {} for _ in range(1, 7)
        }
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                # if class_session_dict.get(curriculum.classroom) is None:
                    # class_session_dict[curriculum.classroom] = {}
                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)], curriculum.week)

                # if grade_course_dict[curriculum.grade].get(time) is None:
                #     grade_course_dict[curriculum.grade][time] = []
                # if curriculum.course_key in grade_course_dict[curriculum.grade][time]:
                #     fitness += cls.weight * len(grade_course_dict[curriculum.grade][time])

                # grade_course_dict[curriculum.grade][time].append(curriculum.course_key)

                # if curriculum.course_type == "選修":
                #     if elective_grade_course_dict[curriculum.grade].get(time) is None:
                #         elective_grade_course_dict[curriculum.grade][time] = []
                #     if curriculum.course_key in elective_grade_course_dict[curriculum.grade][time]:
                #         fitness += cls.weight
                #     elective_grade_course_dict[curriculum.grade][time].append(curriculum.course_key)
                # else:
                #     if compulsory_grade_course_dict[curriculum.grade].get(time) is None:
                #         compulsory_grade_course_dict[curriculum.grade][time] = []
                #     if curriculum.course_key in compulsory_grade_course_dict[curriculum.grade][time]:
                #         fitness += cls.weight
                #     compulsory_grade_course_dict[curriculum.grade][time].append(curriculum.course_key)
                
                # if course_type_grade_course_dict[curriculum.course_type][curriculum.grade].get(time) is None:
                #     course_type_grade_course_dict[curriculum.course_type][curriculum.grade][time] = []
                # if curriculum.course_key in course_type_grade_course_dict[curriculum.course_type][curriculum.grade][time]:
                #     fitness += cls.weight
                # course_type_grade_course_dict[curriculum.course_type][curriculum.grade][time].append(curriculum.course_key)

                if course_type_grade_course_dict[curriculum.grade].get(time) is None:
                    course_type_grade_course_dict[curriculum.grade][time] = False

                if course_type_grade_course_dict[curriculum.grade][time] is True:
                    fitness += cls.weight

                if curriculum.course_type == "必修":
                    course_type_grade_course_dict[curriculum.grade][time] = True


                # if SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 20:
                    # fitness += cls.weight
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        # class_session_dict = {}
        # grade_course_dict = {str(_) : {} for _ in range(1, 7)}

        course_type_grade_course_dict = {
            str(_) : {} for _ in range(1, 7)
        }

        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):


                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)], curriculum.week)

                # if grade_course_dict[curriculum.grade].get(time) is None:
                #     grade_course_dict[curriculum.grade][time] = []
                # if curriculum.course_key in grade_course_dict[curriculum.grade][time]:
                #     if rst[curriculum.course_key].get(cls) is None:
                #         rst[curriculum.course_key][cls] = 0
                #     rst[curriculum.course_key][cls] += 1

                # grade_course_dict[curriculum.grade][time].append(curriculum.course_key)

                # if course_type_grade_course_dict[curriculum.course_type][curriculum.grade].get(time) is None:
                #     course_type_grade_course_dict[curriculum.course_type][curriculum.grade][time] = []
                # if curriculum.course_key in course_type_grade_course_dict[curriculum.course_type][curriculum.grade][time]:
                #     if rst[curriculum.course_key].get(cls) is None:
                #         rst[curriculum.course_key][cls] = 0
                #     rst[curriculum.course_key][cls] += 1
                # course_type_grade_course_dict[curriculum.course_type][curriculum.grade][time].append(curriculum.course_key)


                if course_type_grade_course_dict[curriculum.grade].get(time) is None:
                    course_type_grade_course_dict[curriculum.grade][time] = False
                
                if course_type_grade_course_dict[curriculum.grade][time] is True:
                    if rst[curriculum.course_key].get(cls) is None:
                        rst[curriculum.course_key][cls] = 0
                    rst[curriculum.course_key][cls] += 1

                if curriculum.course_type == "必修":
                    course_type_grade_course_dict[curriculum.grade][time] = True

        return rst