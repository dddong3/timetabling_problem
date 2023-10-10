from typing import Dict

class Bonus:
    def __init__(self, session_list: list[str]):
        self.session_list = session_list

    def rule_1(self, course_week_total: int, is_3_session: bool, session_start_25: bool) -> int:
        return 30 * course_week_total if is_3_session and session_start_25 else 0
