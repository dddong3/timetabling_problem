from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]
@FitnessRegistry.register("ConflictClassroom", weight=-1000)
class ConflictClass(FitnessBase):
    name = "ConflictClassroom"
    show_name = "衝教室"
    description = "If curriculum is conflict classroom, then fitness will be decreased by 100"

    @staticmethod
    def combine_session_week(session, week):
        return str(session) + str(week)

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        class_session_dict = {}
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                if class_session_dict.get(curriculum.classroom) is None:
                    class_session_dict[curriculum.classroom] = {}
                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)], curriculum.week)

                if class_session_dict[curriculum.classroom].get(time, 0) > 0:
                    fitness += cls.weight
                else:
                    class_session_dict[curriculum.classroom][time] = 1

                # if SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 20:
                    # fitness += cls.weight
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        class_session_dict = {}
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                # if SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 20:
                #     if rst[curriculum.course_key].get(cls) is None:
                #         rst[curriculum.course_key][cls] = 0
                #     rst[curriculum.course_key][cls] += 1
                if rst[curriculum.course_key].get(cls) is None:
                    rst[curriculum.course_key][cls] = 0

                if class_session_dict.get(curriculum.classroom) is None:
                    class_session_dict[curriculum.classroom] = {}

                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)], curriculum.week)

                if class_session_dict[curriculum.classroom].get(time, 0) > 0:
                    rst[curriculum.course_key][cls] += 1
                else:
                    class_session_dict[curriculum.classroom][time] = 1

        return rst