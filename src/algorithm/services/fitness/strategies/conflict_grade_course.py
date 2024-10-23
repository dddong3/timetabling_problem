from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]
@FitnessRegistry.register("ConflictGradeCourse", weight=-10000)
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
        course_type_grade_course_dict = {}
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            if course_type_grade_course_dict.get(curriculum.course_class) is None:
                course_type_grade_course_dict[curriculum.course_class] = {}
            for s in range(curriculum.session_length):
                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)], curriculum.week)
                if course_type_grade_course_dict[curriculum.course_class].get(time) is None:
                    course_type_grade_course_dict[curriculum.course_class][time] = False

                if course_type_grade_course_dict[curriculum.course_class][time] is True:
                    fitness += cls.weight

                if curriculum.course_type == "必修":
                    course_type_grade_course_dict[curriculum.course_class][time] = True
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        # class_session_dict = {}
        # grade_course_dict = {str(_) : {} for _ in range(1, 7)}

        course_type_grade_course_dict = {}

        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)], curriculum.week)
                if course_type_grade_course_dict.get(curriculum.course_class) is None:
                    course_type_grade_course_dict[curriculum.course_class] = {}

                if course_type_grade_course_dict[curriculum.course_class].get(time) is None:
                    course_type_grade_course_dict[curriculum.course_class][time] = False
                
                if course_type_grade_course_dict[curriculum.course_class][time] is True:
                    if rst[curriculum.course_key].get(cls) is None:
                        rst[curriculum.course_key][cls] = 0
                    rst[curriculum.course_key][cls] += 1

                if curriculum.course_type == "必修":
                    course_type_grade_course_dict[curriculum.course_class][time] = True

        return rst