from ..abstract import FitnessBase
from ..app import FitnessRegistry

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]
@FitnessRegistry.register("on_02_or_05", weight=-500)
class No20(FitnessBase):
    name = "not_on_02_or_05"
    show_name = "在 02 or 05 or 40 節"
    description = "If curriculum is on 02 or 05, then fitness will be increased by 100"

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            if curriculum.session_length != 3:
                continue

            if not (SESSION_TABLE[session_idx] == 2 or SESSION_TABLE[session_idx] == 5 or SESSION_TABLE[session_idx] == 40):
                fitness += cls.weight
        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        for curriculum in curriculums:
            session_idx = SESSION_TABLE.index(curriculum.session)
            # for s in range(curriculum.session_length):
            #     if SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 2 or SESSION_TABLE[(session_idx + s) % len(SESSION_TABLE)] == 5:
            #         if rst[curriculum.course_key].get(cls) is None:
            #             rst[curriculum.course_key][cls] = 0
            #         rst[curriculum.course_key][cls] += 1
            if curriculum.session_length != 3:
                continue

            if not (SESSION_TABLE[session_idx] == 2 or SESSION_TABLE[session_idx] == 5 or SESSION_TABLE[session_idx] == 40):
                if rst[curriculum.course_key].get(cls) is None:
                    rst[curriculum.course_key][cls] = 0
                rst[curriculum.course_key][cls] += 1

        return rst