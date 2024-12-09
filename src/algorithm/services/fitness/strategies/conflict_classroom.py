from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]
@FitnessRegistry.register("ConflictClassroom", weight=-10000)
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
        class_time_dict = {}
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                if class_time_dict.get(curriculum.classroom) is None:
                    class_time_dict[curriculum.classroom] = {}
                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s)], curriculum.week)

                if class_time_dict[curriculum.classroom].get(time) is None:
                    class_time_dict[curriculum.classroom][time] = []

                if len(class_time_dict[curriculum.classroom][time]):
                    fitness += cls.weight
                class_time_dict[curriculum.classroom][time].append(curriculum)
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        # class_session_dict = {}
        class_time_dict = {}
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                if class_time_dict.get(curriculum.classroom) is None:
                    class_time_dict[curriculum.classroom] = {}

                time = cls.combine_session_week(SESSION_TABLE[(session_idx + s)], curriculum.week)

                if class_time_dict[curriculum.classroom].get(time) is None:
                    class_time_dict[curriculum.classroom][time] = []

                if len(class_time_dict[curriculum.classroom][time]):
                    if rst[curriculum.course_key].get(cls) is None:
                        rst[curriculum.course_key][cls] = 0
                    rst[curriculum.course_key][cls] += 1

                class_time_dict[curriculum.classroom][time].append(curriculum)

                # if class_time_dict[curriculum.classroom].get(time, 0) > 0:
                #     if rst[curriculum.course_key].get(cls) is None:
                #         rst[curriculum.course_key][cls] = 0
                #     rst[curriculum.course_key][cls] += 1

                # class_time_dict[curriculum.classroom][time] = 1


        return rst