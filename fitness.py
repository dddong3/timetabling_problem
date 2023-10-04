from typing import Any


class Fitness():
    START_WEEK, END_WEEK = 1, 5
    session_list = ['01', '02', '03', '04', '20', '05', '06', '07', '08', '09', '40', '50', '60', '70']
    def __init__(self):
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.compute_fitness(*args, **kwds)

    def compute_fitness(self, chromosome: list[dict]) -> int:
        teacher_class_week = {}

        course_week = {}

        fitness = 60
        for gene in chromosome:
            for teacher in gene['teacher_list']:
                if teacher not in teacher_class_week:
                    teacher_class_week[teacher] = {}
                    for week in range(self.START_WEEK, self.END_WEEK + 1):
                        teacher_class_week[teacher][week] = {}
                teacher_session = teacher_class_week[teacher][gene['week']].get(gene['session'], 0)
                teacher_class_week[teacher][gene['week']][gene['session']] = teacher_session + 1
            #建立course_week的邏輯 沒特別check
            if gene['course_id'] not in course_week:
                course_week[gene['course_id']] = {}
                for week in range(self.START_WEEK, self.END_WEEK + 1):
                    course_week[gene['course_id']][str(week)] = {}
            course_session = course_week[gene['course_id']][str(gene['week'])].get(gene['session'], 0)
            course_week[gene['course_id']][str(gene['week'])][gene['session']] = course_session + 1

            #針對單堂課扣分的邏輯可考慮移到course_week底下做
            # penalty rule #4
            fitness -= 100 if gene['session'] == '20' else 0
            # penalty rule #2
            fitness -= 30 if self.session_list.index(gene['session']) > self.session_list.index('07') else 0 

        for teacher in teacher_class_week:
            overtime = False
            working_day = 0
            for week in teacher_class_week[teacher]:
                working_day += 1 if sum(teacher_class_week[teacher][week].values()) > 0 else 0
                overtime |= False if sum(teacher_class_week[teacher][week].values()) <= 6 else True

            # penalty rule #3
            fitness -= 100 if overtime else 0
            # penalty rule #6
            fitness -= 100 if working_day < 3 else 0

        for course in course_week:
            course_week_total = 0
            is_3_session = False
            session_start_25 = False

            for week in course_week[course]:
                # print(course_week[course][week])
                course_week_total += sum(course_week[course][week].values())

                if len(course_week[course][week]) == 3:
                    # print('333', course_week[course][week])
                    session_index = [self.session_list.index(_) for _ in course_week[course][week]]
                    min_index = min(session_index)
                    is_3_session = True if sum(session_index) - 3 * min_index == 3 else False
                    session_start_25 |= True if min_index == self.session_list.index('02') \
                                            or min_index == self.session_list.index('05') else False
                    '''
                    04 20 05 vaild?
                    '''

            if is_3_session:
                # bonus rule #1
                fitness += 30 * course_week_total if session_start_25 else 0
            else:
                # penalty rule #1
                fitness -= 10000 * course_week_total

        return fitness