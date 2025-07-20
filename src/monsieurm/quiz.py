from datetime import date
from typing import Optional

import requests
from pydantic import BaseModel


class Question(BaseModel):
    question: str
    answer: str
    aliases: list[str] = []


class Quiz(BaseModel):
    theme: str
    announcement: Optional[str] = None
    questions: list[Question] = []


def get_quiz(quiz_date: date = date.today()) -> Optional[Quiz]:
    """Load a quiz from femkjappe.no

    Due to the high trust nature of the quiz master, the received object
    contains both questions and answers. It's the caller's responsibility
    not to give answers to the user/LLM too early.

    Args:
        quiz_date (Optional[date]): If set, get the quiz from the specified
            date. If `None`, get the current date.

    Returns:
        A `Quiz` object if a quiz was found, otherwise `None`.

    Raises:
        Any HTTP exception outside of 404 or any parsing errors in the
        returned JSON.
    """
    url = "https://www.femkjappe.no/api/questions?date="
    url += quiz_date.strftime("%Y%m%d")

    res = requests.get(url)

    if res.status_code == 404:
        # Expected when no quiz has been published on a given date, e.g.
        # weekends, dates in the future, or lazy days for the quiz master.
        return None

    res.raise_for_status()

    return Quiz(**res.json())


def is_correct(question: Question, answer: str) -> bool:
    """Check if the answer to a question is correct.

    Args:
        question (Question): The question object we are evaluating, including
            answers and answer aliases. This should come straight from the
            `get_quiz` function.
        answer (str): The suggested answer.

    Returns:
        `True` if the answer is evaluated as correct, `False` otherwise.
    """
    valid_answers = [
        a.lower().strip() for a in [question.answer] + question.aliases
    ]
    answer = answer.lower().strip()

    return answer in valid_answers
