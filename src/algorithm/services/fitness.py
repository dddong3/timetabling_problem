from src.algorithm.models.curriculum import Curriculum

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 30, 40, 50, 60]


class FitnessService:
    def __init__(self):
        pass

    def get_fitness(self, curriculums: list[Curriculum]):
        self.curriculums = curriculums
        fitness = 0
        fitness += self.exceed_time()
        fitness += self.over_07()
        fitness += self.working_overtime()
        fitness += self.no_20()
        # fitness += self.more_work()
        return fitness

    def exceed_time(self) -> int:
        fitness = 0
        for curriculum in self.curriculums:
            if SESSION_TABLE.index(
                curriculum.session
            ) + curriculum.session_length > len(SESSION_TABLE):
                fitness -= 100
        return fitness

    def over_07(self) -> int:
        fitness = 0
        for curriculum in self.curriculums:
            if SESSION_TABLE.index(curriculum.session) > SESSION_TABLE.index(7):
                fitness -= 100
        return fitness

    def working_overtime(self) -> int:
        # TODO : Refactor this method
        fitness = 0
        weekly_teaching_hours = dict()
        for curriculum in self.curriculums:
            if curriculum.week not in weekly_teaching_hours:
                weekly_teaching_hours[curriculum.week] = dict()
            # for teacher in curriculum.teachers:
            teacher = curriculum.teachers
            if teacher not in weekly_teaching_hours[curriculum.week]:
                weekly_teaching_hours[curriculum.week][teacher] = 0
            weekly_teaching_hours[curriculum.week][teacher] += curriculum.session_length

        for week in weekly_teaching_hours:
            for teacher in weekly_teaching_hours[week]:
                if weekly_teaching_hours[week][teacher] > 6:
                    fitness -= 100
        return fitness

    def no_20(self) -> int:
        return (
            -100 if 20 in [curriculum.session for curriculum in self.curriculums] else 0
        )

    # def more_work(self) -> int:
    #     working_day = sum(
    #         1 for week in self.curriculums if sum(week.teachers.values()) > 0
    #     )
    #     return -100 if working_day < 3 else 0


# TODO Add bounus of start on 2 or 5 and 3 sessions
