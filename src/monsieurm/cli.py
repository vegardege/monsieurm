import os
from datetime import date, datetime
from typing import Annotated, Optional

import typer
from rich import print

from monsieurm.llm import answer_question
from monsieurm.quiz import get_quiz

app = typer.Typer()


@app.command()
def display(
    date_string: Annotated[str, typer.Argument()] = date.today().strftime("%Y-%m-%d"),
) -> None:
    """Display the quiz for a specific date"""
    api_key = _load_api_key()
    quiz_date = _parse_quiz_date(date_string)

    if quiz := get_quiz(quiz_date):
        print(quiz.theme)
        print(quiz.announcement)
        for ix, q in enumerate(quiz.questions, start=1):
            print(f"{ix}. {q.question}")
            print(answer_question(q.question, api_key))
    else:
        print(f"No quiz published on {quiz_date.strftime('%Y-%m-%d')}")


def _load_api_key() -> str:
    """Load the API key from the environment variables.

    Returns:
        API key if found.
    """
    try:
        return os.environ["MONSIEURM_API_KEY"]
    except:
        print("❌ Error: Required environment variable 'MONSIEURM_API_KEY' is not set.")
        raise typer.Exit(code=1)


def _parse_quiz_date(input: Optional[str]) -> date:
    """Parse the input string as a date.

    `typer` doesn't support `datetime.date` at the time of writing, so we
    accept an optional `str` and do custom input validation instead.

    Args:
        input (Optional[str]): User input date

    Returns:
        Current date if no user input, otherwise parsed input.
    """
    try:
        return datetime.strptime(input, "%Y-%m-%d").date() if input else date.today()
    except ValueError:
        raise typer.BadParameter("Date must be on the format 'YYYY-MM-DD'")
