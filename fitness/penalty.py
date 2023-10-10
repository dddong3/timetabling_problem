from typing import Dict

class Penalty:
    def __init__(self, session_list: list[str]):
        self.session_list = session_list

    def rule_1(self, course_week_total: int, is_3_session: bool) -> int:
        return -100 * course_week_total if not is_3_session else 0

    def rule_2(self, gene: Dict) -> int:
        return -30 if self.session_list.index(gene['session']) > self.session_list.index('07') else 0

    def rule_3(self, teacher_week: Dict) -> int:
        overtime = any(sum(teacher_week[week].values()) > 6 for week in teacher_week)
        return -100 if overtime else 0

    def rule_4(self, gene: Dict) -> int:
        return -100 if gene['session'] == '20' else 0

    def rule_6(self, teacher_week: Dict) -> int:
        working_day = sum(1 for week in teacher_week if sum(teacher_week[week].values()) > 0)
        return -100 if working_day < 3 else 0
