from ..abstract import FitnessBase
from ..app import FitnessRegistry

from ...custom_rule import CustomRuleService

SESSION_TABLE: list[int] = [1, 2, 3, 4, 20, 5, 6, 7, 8, 9, 40, 50, 60, 70]

custom_rule_service = CustomRuleService()

@FitnessRegistry.register("CustomRules", weight=-10000)
class CustomRules(FitnessBase):
    name = "custom_rule"
    show_name = "Custom Rules"
    description = "If the same grade has the same course, the fitness will be added by 1000."

    @staticmethod
    def combine_session_week(session, week):
        return str(session) + str(week)

    @classmethod
    def evaluate(cls, curriculums):
        fitness = 0
        for curriculum in curriculums:
            if custom_rule_service.check_common_deny_time_conflict(curriculum):
                fitness += cls.weight
            if custom_rule_service.check_course_requirement_time_conflict(curriculum):
                fitness += cls.weight
            if custom_rule_service.check_teacher_deny_time_conflict(curriculum):
                fitness += cls.weight

        return fitness
    
    @classmethod
    def record(cls, curriculums, rst):
        # class_session_dict = {}
        # grade_course_dict = {str(_) : {} for _ in range(1, 7)}


        for curriculum in curriculums:
            if custom_rule_service.check_common_deny_time_conflict(curriculum):
                if rst[curriculum.course_key].get(cls) is None:
                    rst[curriculum.course_key][cls] = 0
                rst[curriculum.course_key][cls] += 1

            if custom_rule_service.check_course_requirement_time_conflict(curriculum):
                if rst[curriculum.course_key].get(cls) is None:
                    rst[curriculum.course_key][cls] = 0
                rst[curriculum.course_key][cls] += 1

            if custom_rule_service.check_teacher_deny_time_conflict(curriculum):
                if rst[curriculum.course_key].get(cls) is None:
                    rst[curriculum.course_key][cls] = 0
                rst[curriculum.course_key][cls] += 1

        return rst