from .abstract import FitnessBase
from src.algorithm.models.curriculum import Curriculum
import json

class FitnessRegistry:
    strategies = {}
    # weights = {}
    skip_list = [
        # "ConflictGradeCourse",
        # "over_09",
        # "no_20",
        # "ConflictTeacher",
        # "over_70",
        # "ConflictClassroom",
        # "exceed_time"
    ]

    @classmethod
    def register(cls, strategy, weight):
        def decorator(subclass):
            if strategy in cls.skip_list:
                return subclass
            cls.strategies[strategy] = subclass
            # cls.weights[strategy] = weight
            subclass.weight = weight
            print(f"Register {subclass} to {strategy}")
            return subclass
        
        return decorator
    
    @classmethod
    def get_strategy(cls, strategy) -> FitnessBase:
        if strategy not in cls.strategies:
            raise ValueError(f"Unknown fitness strategy {strategy}")
        return cls.strategies[strategy]
    
    @classmethod
    def get_strategies(cls):
        return cls.strategies.values()
    
fitness_registry = FitnessRegistry()

class FitnessService:
    def __init__(self):
        pass

    def get_fitness(self, curriculums: list[Curriculum]):
        fitness = 0
        for strategy in FitnessRegistry.get_strategies():
            # strategy.weight = FitnessRegistry.weights[strategy.name]
            fitness += strategy.evaluate(curriculums)
        return fitness
    
    def record(self, curriculums: list[Curriculum]):
        rst = {}

        # print(f'strategies: {FitnessRegistry.get_strategies()}')

        for curriculum in curriculums:
            rst[curriculum.course_key] = {}

        for strategy in FitnessRegistry.get_strategies():
            rst = strategy.record(curriculums, rst)

        opt = []

        for k, v in rst.items():
            opt.append({
                "course_key": k,
                "fitness": [{
                    "rule": kk.name,
                    "count": vv,
                    "weight": kk.weight,
                    "score": kk.weight * vv
                } for kk, vv in v.items()]
            })

        return opt
    
    def record_and_output(self, filename:str, curriculums: list[Curriculum]):
        # rst = {}

        print(f'strategies: {FitnessRegistry.get_strategies()}')

        # for curriculum in curriculums:
        #     rst[curriculum.course_key] = {}

        # for strategy in FitnessRegistry.get_strategies():
        #     rst = strategy.record(curriculums, rst)

        # opt = []

        # for k, v in rst.items():
        #     opt.append({
        #         "course_key": k,
        #         "fitness": [{
        #             "rule": kk.name,
        #             "count": vv
        #         } for kk, vv in v.items()]
        #     })

        rst = self.record(curriculums)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(rst, ensure_ascii=False, indent=4))
    
    def output_rule(self):
        with open("data/results/rules.json", "w", encoding="utf-8") as f:
            f.write(json.dumps([{
                "name": strategy.name,
                "show_name": strategy.show_name,
                "description": strategy.description,
                "weight": strategy.weight
            } for strategy in FitnessRegistry.get_strategies()], ensure_ascii=False, indent=4)
            )