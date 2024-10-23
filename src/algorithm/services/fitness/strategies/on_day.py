from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]
@FitnessRegistry.register("on_day", weight=-100)
class NoDay(FitnessBase):
    name = "on_day"
    show_name = "在早上"
    description = "If curriculum is on 02 or 05, then fitness will be increased by 100"

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            # if session_idx + curriculum.session_length >= SESSION_TABLE.index(40):
                # fitness += cls.weight
            fitness += cls.weight * session_idx
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        # for curriculum in curriculums:
            # session_idx = SESSION_TABLE.index(curriculum.session)

            # if session_idx + curriculum.session_length >= SESSION_TABLE.index(40):
            #     if rst[curriculum.course_key].get(cls) is None:
            #         rst[curriculum.course_key][cls] = 0
            #     rst[curriculum.course_key][cls] += 1

        return rst