![Monsieur Mistral](https://raw.githubusercontent.com/vegardege/monsieurm/refs/heads/main/assets/monsieurm.png?raw=true)

# Monsieur Mistral

Slack Bot solving the daily quiz [Fem Kjappe](https://www.femkjappe.no/) using
Mistral's API and updates a Slack channel with the LLM's score and a reaction.

This bot was built as part of a man vs machine battle at
[Zerolytics](https://www.zerolytics.com), and was not designed to be used
outside our universe.

## Installation

Open source in the spirit of sharing and learning. In the obscure event you
want to set it up and run it yourself, the easiest way it:

1. Get an API key from Mistral and set it to `MONSIEURM_MISTRAL_API_KEY`
   in your environment.
2. If you want to post scores and reactions to a Slack channel, create a Slack
   bot in your workspace, generate a token for it (`chat:write` and
   `chat:write.public` required permissions) and set the token to
   `MONSIEURM_SLACK_TOKEN`.

## Usage

Then run it every week day using:

```bash
monsieurm solve --post-slack
```

You can also specify a date to solve and publish previous quiz.

If you want to see the answers, run:

```bash
monsieurm display
```

But note that the output will contain spoilers to the quiz, so make sure you
solved it yourself first.

Because human participants aren't allowed to use any help, Mistral is of
course not given any tools or the option to search. This is man vs machine
at its most honest and brutal.
