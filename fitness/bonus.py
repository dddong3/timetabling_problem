from typing import Dict

class Bonus:
    def __init__(self, session_list: list[str]):
        self.session_list = session_list

    def rule_1(self, course_time_dict: dict) -> int:
        fitness = 0
        for course in course_time_dict:
            #course_time_set = {(classroom, week)}
            course_time_set = set(tuple(val[:2]) for val in course_time_dict[course])
            if len(course_time_set) == 1:
                course_session_list = [val[2] for val in course_time_dict[course]]
                course_session_idx = [self.session_list.index(val) for val in course_session_list]
                course_session_idx.sort()
                if course_session_idx[0] == 1 or course_session_idx[0] == 5:
                    fitness += 100 * len(course_time_dict[course])
        return fitness
