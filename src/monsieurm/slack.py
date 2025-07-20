from slack_sdk import WebClient

# This Slack channel needs to be available in the Workspace the bot was
# installed for. It could be an env var if we were picky, but if you're
# actually using this script, you're probably forking it anyway.
CHANNEL = "#dagens-quiz"


def generate_slack_message(theme: str, emojis: str, reaction: str) -> str:
    """Generate a Slack message we can print or post.

    Args:
        theme (str): Daily quiz theme.
        emojis (str): Score as emojis, similar to femkjappe.no.
        reaction (str): Reaction to the score from the LLM.

    Returns:
        A Slack friendly message
    """
    return f"{reaction}\n\n{emojis}\nDagens tema: {theme}"


def post_slack_message(message: str, slack_token: str) -> None:
    """Post a message to the configured Slack channel.

    Args:
        message (str): The formatted message to post.
        slack_token (str): Secret token from Slack.
    """
    client = WebClient(token=slack_token)
    client.chat_postMessage(channel=CHANNEL, text=message)
