# Monsieur Mistral

An AI participant in the Norwegian daily quiz
[Fem Kjappe](https://www.femkjappe.no/).

The bot uses Mistral's API to answer five daily questions, check his own
results, then posts his scores and a reaction to our dedicated quiz
Slack channel:

![Slack screenshot](https://raw.githubusercontent.com/vegardege/monsieurm/refs/heads/main/assets/screenshot.png?raw=true)

The script was built for internal use at
[Zerolytics](https://www.zerolytics.com), and was not designed for external
reuse or distribution. Open source in the spirit of sharing and learning.

## Installation

> [!NOTE]
> You almost certainly need to change a few things in the code if you want
> to run this in a different setting. This guide assumes you're deploying
> the bot internally at Zerolytics.

The easiest way to get started is with [Poetry](https://python-poetry.org/):

### Prerequisites

1. **Install Poetry**  
   Follow the instructions at
   [python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).

2. **Set Environment Variables**
   - Get an API key from [Mistral](https://mistral.ai/) and set it:
     ```bash
     export MONSIEURM_MISTRAL_API_KEY=<your_mistral_api_key>
     ```
   - (Optional) To post scores and reactions to Slack:
     - Create a [Slack bot](https://api.slack.com/apps/) in your workspace.
     - Grant it the following permissions: `chat:write` and `chat:write.public`.
     - Set your bot token:
       ```bash
       export MONSIEURM_SLACK_TOKEN=<your_slack_token>
       ```

### Install Dependencies

```bash
poetry install
```

## Usage

Run the tool once per weekday with:

```bash
poetry run monsieurm solve --post-slack
```

To solve and publish a past quiz for a specific date:

```bash
poetry run monsieurm solve 2025-07-18
```

To view answers:

```bash
poetry run monsieurm display
```

You can also provide a date to display results for a past quiz.

> [!WARNING]
> The output of `display` will contain spoilers to the quiz when the LLM gets
> an answer right, so make sure you solved it yourself before running it.

Because human participants aren't allowed to use any help, Mistral is of
course _not_ given any tools or the option to search. This is man vs
machine at its most honest and brutal.
