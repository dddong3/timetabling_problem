from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]
@FitnessRegistry.register("ConflictTeacher", weight=-1000)
class ConflictTeacher(FitnessBase):
    name = "ConflictTeacher"
    show_name = "衝老師"
    description = "If curriculum is conflict teacher, then fitness will be decreased by 100"

    @staticmethod
    def combine_session_week(session, week):
        return str(session) + str(week)

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        teacher_session_dict = {}
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                if teacher_session_dict.get(curriculum.teachers) is None:
                    teacher_session_dict[curriculum.teachers] = {}
                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)], curriculum.week)

                if teacher_session_dict[curriculum.teachers].get(time, 0) > 0:
                    fitness += cls.weight
                else:
                    teacher_session_dict[curriculum.teachers][time] = 1

                # if SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 20:
                    # fitness += cls.weight
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        teacher_session_dict = {}
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                # if SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 20:
                #     if rst[curriculum.course_key].get(cls) is None:
                #         rst[curriculum.course_key][cls] = 0
                #     rst[curriculum.course_key][cls] += 1
                
                # if rst[curriculum.course_key].get(cls) is None:
                #     rst[curriculum.course_key][cls] = 0

                if teacher_session_dict.get(curriculum.teachers) is None:
                    teacher_session_dict[curriculum.teachers] = {}

                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)], curriculum.week)

                if rst[curriculum.course_key].get(cls) is None:
                    rst[curriculum.course_key][cls] = 0

                if teacher_session_dict[curriculum.teachers].get(time, 0) > 0:
                    rst[curriculum.course_key][cls] += 1
                else:
                    teacher_session_dict[curriculum.teachers][time] = 1

        return rst