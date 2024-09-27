from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]

@FitnessRegistry.register("over_09", weight=-10)
class Over07(FitnessBase):
    name = "over_09"
    show_name = "超過 09 節"
    description = "If curriculum is over 09, then fitness will be decreased by 100"

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        for curriculum in curriculums:
            if SESSION_TABLE.index(curriculum.session) > SESSION_TABLE.index(9):
                fitness += cls.weight
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        for curriculum in curriculums:
            if SESSION_TABLE.index(curriculum.session) > SESSION_TABLE.index(9):
                if rst[curriculum.course_key].get(cls) is None:
                    rst[curriculum.course_key][cls] = 0
                rst[curriculum.course_key][cls] += 1

        return rst