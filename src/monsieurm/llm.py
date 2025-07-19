import time
from typing import Optional

import requests
from requests.exceptions import HTTPError

from monsieurm.prompts import QUESTION_PROMPT, REACTION_PROMPT

ROOT_URL = "https://api.mistral.ai"


class LLMException(Exception):
    pass


def answer_question(question: str, api_key: str) -> str:
    """Ask a quiz question to the LLM and get a response.

    Args:
        question (str): Question from the quiz.
        api_key (str): Bearer token provided by Mistral after signup.
    """
    return _chat_completion(QUESTION_PROMPT.format(question=question), api_key)


def reaction_from_score(score: int, api_key: str) -> str:
    """Ask a quiz question to the LLM and get a response.

    Args:
        question (str): Question from the quiz.
        api_key (str): Bearer token provided by Mistral after signup.
    """
    return _chat_completion(REACTION_PROMPT.format(score=score), api_key)


def _chat_completion(prompt: str, api_key: str, sleep: Optional[float] = 1.0) -> str:
    """Simple wrapper around Mistral's chat completion API.

    This function assumes a simple prompt from the user, and a single response
    from the assistant. Expand if more advanced functionality (e.g. tools) is
    needed. Switch to the SDK if needs become more advanced.
    """
    url = f"{ROOT_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    json = {
        "model": "mistral-medium-latest",
        "messages": [
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    try:
        res = requests.post(url, headers=headers, json=json)
        res.raise_for_status()

        response_content = res.json()["choices"][0]["message"]["content"]

        if sleep:
            # Mistral's free tier only allows one request per second.
            # This is a super simple way of respecting that.
            time.sleep(sleep)

        return response_content

    except HTTPError as e:
        raise LLMException(f"HTTP Error: {e}")
    except KeyError as e:
        raise LLMException(f"Invalid response from LLM: {e}")
    except Exception as e:
        raise LLMException(f"Unexpected error: {e}")
