from dataclasses import dataclass

@dataclass
class Step:
    step: int
    complete: bool

@dataclass
class Course:
    name: str
    step_count: int
    steps: list[Step]


courses_to_words = {
    "Ценные бумаги": "paper",
    "Личный и семейный бюджет": "money",
    "Как выйти на пенсию в 35 лет": "35"
}

words_to_courses = {v: k for k, v in courses_to_words.items()}

