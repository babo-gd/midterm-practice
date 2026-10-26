"""연습용 가짜 문제: 학생 성적 관리 시스템

[가짜 문제지 요구사항]
- class StudentManager
  - add_student(name: str, score: int) -> bool
      이름이 비어 있거나, 점수가 0~100 밖이거나, 이미 있는 이름이면 False
      성공하면 True
  - get_average() -> float
      전체 평균 (소수 둘째 자리 반올림), 학생이 없으면 0.0
  - get_grade(name: str) -> str
      90 이상 A, 80 이상 B, 70 이상 C, 60 이상 D, 그 외 F
      없는 학생이면 "NOT_FOUND"
  - get_top(n: int) -> list[str]
      점수 높은 순 n명의 이름 (점수가 같으면 이름 가나다/알파벳 순)
      n이 0 이하면 빈 리스트
"""


class StudentManager:
    def __init__(self):
        self.scores = {}

    def add_student(self, name, score):
        if not isinstance(name, str) or not name.strip():
            return False
        if not isinstance(score, int) or isinstance(score, bool):
            return False
        if score < 0 or score > 100:
            return False
        if name in self.scores:
            return False
        self.scores[name] = score
        return True

    def get_average(self):
        if not self.scores:
            return 0.0
        return round(sum(self.scores.values()) / len(self.scores), 2)

    def get_grade(self, name):
        if name not in self.scores:
            return "NOT_FOUND"
        s = self.scores[name]
        if s >= 90:
            return "A"
        if s >= 80:
            return "B"
        if s >= 70:
            return "C"
        if s >= 60:
            return "D"
        return "F"

    def get_top(self, n):
        if not isinstance(n, int) or n <= 0:
            return []
        ranked = sorted(self.scores.items(), key=lambda kv: (-kv[1], kv[0]))
        return [name for name, _ in ranked[:n]]
