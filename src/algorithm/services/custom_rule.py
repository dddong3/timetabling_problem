import json

from src.algorithm.services.school_curriculum import SchoolCurriculumService

school_curriculum_service = SchoolCurriculumService()

TIME_TABLE = {
    1: [1, 2, 3, 4],
    2: [5, 6, 7, 8, 9],
    3: [40, 50, 60, 70]
}

class CustomRuleService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CustomRuleService, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self._rules = {}
        self._common_deny_time = {_: [] for _ in range(1, 6)}
        self._course_requirement_time = {}
        self._teacher_deny_time = {}

        with open("data/course/rules.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # for rule in data:
        #     rule_type = rule["rule_type"]
        #     if rule_type not in self._rules:
        #         self._rules[rule_type] = []
        #     self._rules[rule_type].append(rule)
        # print(self._rules)
        # for rule in self._rules:
        for rule in data:
            if rule["rule_type"] == "common_deny_time":
                for time in rule["deny_time"]:
                    for grade in rule["grade"]:
                        t = TIME_TABLE[int(time["time"])]
                        for _ in t:
                            self._common_deny_time[grade].append(f'{time["weekday"]}/{_}')
            elif rule["rule_type"] == "common_deny_time_period":
                for time in rule["deny_time"]:
                    for grade in rule["grade"]:
                        self._common_deny_time[grade].append(f'{time["weekday"]}/{time["period"]}')
            elif rule["rule_type"] == "course_requirement_time":
                self._course_requirement_time[rule["course_key"]] = f'{rule["time"]["weekday"]}/{rule["time"]["period"]}'
            elif rule["rule_type"] == "teacher_deny_time":
                if rule["teacher_name"] not in self._teacher_deny_time:
                    self._teacher_deny_time[rule["teacher_name"]] = []
            else:
                raise NotImplementedError(f"Rule type {rule['rule_type']} is not implemented.")
        print(self._common_deny_time)
                
    def check_common_deny_time_conflict(self, curriculum):
        curriculum_time = f'{curriculum.week}/{curriculum.session}'
        if curriculum_time in self._common_deny_time[int(curriculum.grade)]:
            return True
        return False
    
    def check_course_requirement_time_conflict(self, curriculum):
        curriculum_time = f'{curriculum.week}/{curriculum.session}'
        if curriculum.course_key in self._course_requirement_time and curriculum_time != self._course_requirement_time[curriculum.course_key]:
            return True
        return False
    
    def check_teacher_deny_time_conflict(self, curriculum):
        curriculum_time = f'{curriculum.week}/{curriculum.session}'
        teacher_list = school_curriculum_service.get_teacher_by_id(curriculum.teachers)

        for teacher in teacher_list:
            if teacher in self._teacher_deny_time and curriculum_time in self._teacher_deny_time[teacher]:
                return True
            
        return False
    
    def check_course_key_in_rule(self, course_key):
        return course_key in self._course_requirement_time
    
    def get_requirement_time_by_course_key(self, course_key):
        return self._course_requirement_time[course_key]
