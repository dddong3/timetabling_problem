from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]

@FitnessRegistry.register("over_70", weight=-1000)
class Over07(FitnessBase):
    name = "over_70"
    show_name = "超過 70 節"
    description = "If curriculum is over 70, then fitness will be decreased by 100"

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        for curriculum in curriculums:
            for s in range(curriculum.session_length):
                
                if SESSION_TABLE.index(curriculum.session) + s > len(SESSION_TABLE) - 1:
                    fitness += cls.weight
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        for curriculum in curriculums:
            for s in range(curriculum.session_length):
                if SESSION_TABLE.index(curriculum.session) + s > len(SESSION_TABLE) - 1:
                    if rst[curriculum.course_key].get(cls) is None:
                        rst[curriculum.course_key][cls] = 0
                    rst[curriculum.course_key][cls] += 1
            # if SESSION_TABLE.index(curriculum.session) > SESSION_TABLE.index(7):
            #     if rst[curriculum.course_key].get(cls) is None:
            #         rst[curriculum.course_key][cls] = 0
            #     rst[curriculum.course_key][cls] += 1

        return rst