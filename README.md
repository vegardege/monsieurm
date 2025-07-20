# Monsieur Mistral

![Monsieur Mistral](https://raw.githubusercontent.com/vegardege/monsieurm/refs/heads/main/assets/monsieurm.png?raw=true)

An AI participant in the Norwegian daily quiz
[Fem Kjappe](https://www.femkjappe.no/).

The bot uses Mistral's API to answer the daily questions, and posts scores
and a reaction to our internal Slack channel.

The script was built for internal use at
[Zerolytics](https://www.zerolytics.com), and was not designed for external
reuse or distribution. Open source in the spirit of sharing and learning.

## Installation

You almost certainly need to change a few things if you want to set this up
in a different context than ours.

The easiest way to get the script running is by using `poetry` with a couple
of secret env vars:

1. Install [poetry](https://python-poetry.org/docs/#installation)
2. Get an API key from Mistral and set it to `MONSIEURM_MISTRAL_API_KEY`
   in your environment.
3. If you want to post scores and reactions to a Slack channel, create a Slack
   bot in your workspace, generate a token for it (`chat:write` and
   `chat:write.public` required permissions) and set the token to
   `MONSIEURM_SLACK_TOKEN`.
4. Execute `poetry install`
5. For each run, execute `poetry run monsieurm`

## Usage

The tool should be run once per week day using:

```bash
poetry run monsieurm solve --post-slack
```

You can also specify a date to solve and publish previous quiz:

```bash
poetry run monsieurm solve 2025-07-18
```

If you want to see the answers, run:

```bash
poetry run monsieurm display
```

Again with an optional date.

> [!WARNING]
> The output of `display` will contain spoilers to the quiz when the LLM gets
> an answer right, so make sure you solved it yourself before running it.

Because human participants aren't allowed to use any help, Mistral is of
course _not_ given any tools or the option to search. This is man vs
machine at its most honest and brutal.
