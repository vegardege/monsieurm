import random
import time
from typing import Optional

import requests

from monsieurm.prompts import (
    QUESTION_PROMPT,
    REACTION_PROMPT,
    REACTION_VARIATION,
)

ROOT_URL = "https://api.mistral.ai"


def answer_question(question: str, api_key: str) -> str:
    """Ask a quiz question to the LLM and get a response.

    Temperature set to 0.0 to ensure deterministic answers with no
    creativity.

    Args:
        question (str): Question from the quiz.
        api_key (str): Bearer token provided by Mistral after signup.
    """
    return _chat_completion(
        QUESTION_PROMPT.format(question=question),
        api_key,
        temperature=0.0,
    )


def reaction_from_score(score: int, api_key: str) -> str:
    """Ask a quiz question to the LLM and get a response.

    Args:
        question (str): Question from the quiz.
        api_key (str): Bearer token provided by Mistral after signup.
    """
    variation = random.choice(REACTION_VARIATION)
    return _chat_completion(
        REACTION_PROMPT.format(score=score, variation=variation),
        api_key,
        temperature=1.0,
    )


def _chat_completion(
    prompt: str,
    api_key: str,
    temperature: float,
    sleep: Optional[float] = 1.0,
) -> str:
    """Simple wrapper around Mistral's chat completion API.

    This function assumes a simple prompt from the user, and a single response
    from the assistant. Expand if more advanced functionality (e.g. tools) is
    needed. Switch to the SDK if needs become more advanced.

    Note that we're setting a fixed random seed. This allows us to reproduce a
    run and see what it answered if we're curious.
    """
    url = f"{ROOT_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    json = {
        "model": "mistral-medium-latest",
        "temperature": temperature,
        "random_seed": 0,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    res = requests.post(url, headers=headers, json=json)
    res.raise_for_status()

    response_content = res.json()["choices"][0]["message"]["content"]

    if sleep:
        # Mistral's free tier only allows one request per second.
        # This is a super simple way of respecting that.
        time.sleep(sleep)

    return response_content
