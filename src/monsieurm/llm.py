import time
from typing import Optional

import requests
from requests.exceptions import HTTPError

ROOT_URL = "https://api.mistral.ai"

PROMPT = """Du deltar i en online quiz og skal svare korrekt på dagens spørsmål.
Viktig: svaret ditt evalueres maskinelt, du må derfor ikke svare noe annet enn
selve svaret på spørsmålet. All annen tekst vil medføre at du får 0 poeng.

= EKSEMPEL =

Hva er hovedstaden i Tyskland?
Berlin

Hvem er grunnstoff nummer 107 oppkalt etter?
Niels Bohr

= DAGENS SPØRSMÅL =
"""


class LLMException(Exception):
    pass


def answer_question(question: str, api_key: str, sleep: Optional[float] = 1.0) -> str:
    """Simple wrapper around Mistral's chat completion API.

    This function assumes a simple question from the user, and a single response
    from the assistant. Expand if more advanced functionality (e.g. tools) is
    needed. Switch to the SDK if needs become more advanced.

    Args:
        question (str): Question from the user.
        api_key (str): Bearer token provided by Mistral after signup.
        sleep (float): Seconds to sleep after the request.

    Returns:
        Answer from the assistant.
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
                "content": PROMPT + question,
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
