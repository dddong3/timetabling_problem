import time
import json
import random
from chromosome_fitness import Fitness

class GeniticAlgoithm:
    START_WEEK, END_WEEK = 1, 5
    session_list = ['01', '02', '03', '04', '20', '05', '06', '07', '08', '09', '40', '50', '60', '70']
    livecycle = None
    gene_list = None
    class_list = None
    class_detail = None
    population_size = None
    def __init__(self: object) -> None:
        assert(self.START_WEEK <= self.END_WEEK)
        assert(self.population_size is not None)
        assert(self.livecycle is not None)
        assert(self.gene_list is not None)
        assert(self.class_detail is not None)
        assert(self.class_list is not None)

        self.best_fitness = None
        self.best_chromosome = None
        # self.__fitness = [self.cal_fitness(chromosome) for chromosome in self.__chromosome]
        self.run()
        # print(self.best_fitness)

    @classmethod
    def init(cls, courseFileName: str, classFileName: str, *, popu: int, live: int) -> None:
        cls.population_size = popu
        cls.livecycle = live
        cls.gene_list = GeniticAlgoithm.get_json(courseFileName)
        cls.class_detail = GeniticAlgoithm.get_json(classFileName)
        cls.class_list = list(cls.class_detail.keys())


    def __lt__(self: object, other: object) -> bool:
        return self.best_fitness < other.best_fitness

    def run(self: object) -> None:
        self.chromosome = [self.generate_chromosome() for _ in range(self.population_size)]
        self.fitness = [self.cal_fitness(chromosome) for chromosome in self.chromosome]
        self.update_best_fitness()
        for _ in range(self.livecycle):
            self.cross_over()
            self.update_best_fitness()
            self.mutation()
            self.update_best_fitness()
            self.selection()

    def update_best_fitness(self: object) -> None:
        self.best_fitness = max(self.fitness)
        self.best_chromosome = self.chromosome[self.fitness.index(self.best_fitness)]
    
    def cross_over(self: object) -> None:
        self.chromosome.extend([self.generate_chromosome() for _ in range(self.population_size)])
        self.fitness.extend([self.cal_fitness(chromosome) for chromosome in self.chromosome[self.population_size:]])

    def mutation(self: object) -> None:
        pass

    def selection(self: object) -> None:
        self.chromosome = [chromosome for _, chromosome in sorted(zip(self.fitness, self.chromosome), reverse=True)]
        self.fitness = sorted(self.fitness, reverse=True)
        self.chromosome = self.chromosome[:self.population_size]
        self.fitness = self.fitness[:self.population_size]

    def output_chromosome(self: object) -> None:
        fileName = f'chromosome_{self.best_fitness}_{time.strftime("%m%d%H%M", time.localtime())}.json'
        json.dump(self.best_chromosome, open(fileName, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    @staticmethod
    def get_json(fileName: str) -> dict:
        return json.load(open(fileName, 'r', encoding='utf-8'))

    def generate_chromosome(self: object) -> list[list[dict]]:
        '''
        chromosome =
        [
            {
                'course_id': "12345",
                'teacher_list': [
                    'teacher_1',
                    'teacher_2'
                ],
                'week': 1,
                'session': '20',
                'classroom': 'A101'
            }
        ]        
        '''
        chromosome = self.gene_list.copy()
        for course in chromosome:
            course['week'] = random.randint(self.START_WEEK, self.END_WEEK)
            course['session'] = random.choice(self.session_list)
            course['classroom'] = random.choice(self.class_list)
        return chromosome
    
    def cal_fitness(self: object, chromosome: list[dict]) -> int:
        teacher_class_week = {}
        '''
        teacher_class_week = 
        {
            'teacher_1': {
                1: {
                    '01': 2,
                    '02': 1,
                    '03': 0,
                    ...
                }
                2: {
                    '01': 2,
                    '02': 1,
                    '03': 0,
                    ...
                },
                ...
            },
        }

        if 規則太多改成加分fun和減分fun維護
        '''

        course_week = {}
        '''
        course_week =
        {
            '12345': {
                '1': {
                    '01': 2,
                    '02': 1,
                    '03': 0,
                    ...
                }
            }
        }
        '''


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