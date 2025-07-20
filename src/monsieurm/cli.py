from datetime import date, datetime
from typing import Annotated, Optional

import typer
from rich import print

from monsieurm.config import load_config
from monsieurm.llm import answer_question, reaction_from_score
from monsieurm.quiz import get_quiz, is_correct
from monsieurm.slack import generate_slack_message, post_slack_message

app = typer.Typer()

TODAY = date.today().strftime("%Y-%m-%d")


@app.command()
def solve(
    date: Annotated[
        str,
        typer.Argument(help="Quiz date (YYYY-MM-DD)"),
    ] = TODAY,
    post_slack: Annotated[
        bool,
        typer.Option(help="Post result to Slack"),
    ] = False,
) -> None:
    """Solve the quiz for a specific date and post results to Slack."""
    config = load_config()
    quiz_date = _parse_quiz_date(date)

    score = 0
    emojis = ""

    if quiz := get_quiz(quiz_date):
        for q in quiz.questions:
            question = q.question
            answer = answer_question(question, config.mistral_api_key)

            if is_correct(q, answer):
                score += 1
                emojis += "🟩"
            else:
                emojis += "🟥"

        reaction = reaction_from_score(score, config.mistral_api_key)
        message = generate_slack_message(quiz.theme, emojis, reaction)

        if post_slack and config.slack_bot_token:
            post_slack_message(message, config.slack_bot_token)
        else:
            print(message)
    else:
        print(f"No quiz published on {quiz_date.strftime('%Y-%m-%d')}")


@app.command()
def display(
    date: Annotated[
        str,
        typer.Argument(help="Quiz date (YYYY-MM-DD)"),
    ] = TODAY,
) -> None:
    """Display the quiz for a specific date with LLM answers."""
    config = load_config()
    quiz_date = _parse_quiz_date(date)

    if quiz := get_quiz(quiz_date):
        print(f"❓ {quiz.theme}")

        if quiz.announcement:
            print(f"❗ {quiz.announcement}")

        for ix, q in enumerate(quiz.questions, start=1):
            question = q.question
            answer = answer_question(question, config.mistral_api_key)
            correct = is_correct(q, answer)
            emoji = "🟩" if correct else "🟥"

            print()
            print(f"{ix}. {question}")
            print(f"{emoji} {answer}")
    else:
        print(f"No quiz published on {quiz_date.strftime('%Y-%m-%d')}")


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
        return (
            datetime.strptime(input, "%Y-%m-%d").date()
            if input
            else date.today()
        )
    except ValueError:
        raise typer.BadParameter("Date must be on the format 'YYYY-MM-DD'")
