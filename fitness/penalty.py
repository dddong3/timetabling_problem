from typing import Dict

class Penalty:
    def __init__(self, session_list: list[str]):
        self.session_list = session_list

    def exceed_time(self, chromosome: list[object]) -> int:
        fitness = 0
        for course in chromosome:
            session_idx = self.session_list.index(course['session'])
            if session_idx + course['session_length'] > len(self.session_list):
                fitness -= 100
        return fitness

    def over_07(self,chromosome: list[object]) -> int:
        fitness = 0
        for course in chromosome:
            if self.session_list.index(course['session']) > self.session_list.index('07'):
                fitness -= 100
        return fitness

    def working_overtime(self, chromosome: list[object]) -> int:
        fitness = 0
        weekly_teaching_hours = dict()
        for course in chromosome:
            if course['week'] not in weekly_teaching_hours:
                weekly_teaching_hours[course['week']] = dict()
            for teacher in course['teacher_list']:
                if teacher not in weekly_teaching_hours[course['week']]:
                    weekly_teaching_hours[course['week']][teacher] = 0
                weekly_teaching_hours[course['week']][teacher] += course['session_length']
        
        for week in weekly_teaching_hours:
            for teacher in weekly_teaching_hours[week]:
                if weekly_teaching_hours[week][teacher] > 6:
                    fitness -= 100
        return fitness


    def rule_4(self, gene: Dict) -> int:
        return -100 if gene['session'] == '20' else 0

    def rule_6(self, teacher_week: Dict) -> int:
        working_day = sum(1 for week in teacher_week if sum(teacher_week[week].values()) > 0)
        return -100 if working_day < 3 else 0
