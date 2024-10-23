from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]
@FitnessRegistry.register("no_20", weight=-10000)
class No20(FitnessBase):
    name = "no_20"
    show_name = "在 20 節"
    description = "If curriculum is no 20, then fitness will be decreased by 100"

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                if SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 20:
                    fitness += cls.weight
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            for s in range(curriculum.session_length):
                if SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 20:
                    if rst[curriculum.course_key].get(cls) is None:
                        rst[curriculum.course_key][cls] = 0
                    rst[curriculum.course_key][cls] += 1

        return rst