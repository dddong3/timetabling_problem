from typing import Dict

class Bonus:
    def __init__(self, session_list: list[str]):
        self.session_list = session_list

    def start_on_2_5(self, chromosome: list[object]) -> int:
        fitness = 0
        for course in chromosome:
            if course['session'] == '02' or course['session'] == '05':
                fitness += 50
        return fitness
