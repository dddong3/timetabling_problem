from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]

@FitnessRegistry.register("exceed_time", weight=-1000)
class ExceedTime(FitnessBase):
    name = "exceed_time"
    show_name = "超時工作"
    description = "If curriculum is exceed time, then fitness will be decreased by 100"

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        for curriculum in curriculums:
            if SESSION_TABLE.index(
                curriculum.session
            ) + curriculum.session_length > len(SESSION_TABLE):
                fitness += cls.weight
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        for curriculum in curriculums:
            if SESSION_TABLE.index(
                curriculum.session
            ) + curriculum.session_length > len(SESSION_TABLE):
                if rst[curriculum.course_key].get(cls) is None:
                    rst[curriculum.course_key][cls] = 0
                rst[curriculum.course_key][cls] += 1

        return rst