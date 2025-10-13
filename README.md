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

`monsieurm` needs a [Mistral](https://mistral.ai/) API token to run. If you
want to post updates to [Slack bot](https://api.slack.com/apps/), you need
a Slack token as well, but this is optional.

The easiest way to get started is by using [docker](https://docker.com):

```bash
docker build -t monsieurm:latest .
cp .env.template .env # Add your secrets to the .env file
docker run --rm -it --env-file .env monsieurm display 2025-08-01
```

If you want to use [uv](https://docs.astral.sh/uv/) directly:

1. **Install uv**
   Follow the instructions at
   [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/).

2. **Set Environment Variables**

   ```bash
   export MONSIEURM_MISTRAL_API_KEY=<your_mistral_api_key>
   export MONSIEURM_SLACK_TOKEN=<your_slack_token>
   ```

3. Install Dependencies

   ```bash
   uv sync
   ```

4. Run tool:

   ```bash
   uv run monsieurm solve --post-slack
   ```

   If `.venv/bin` or your uv environment is in your PATH, you can run the CLI directly:

   ```bash
   monsieurm solve --post-slack
   ```

## Usage

To solve and publish a past quiz for a specific date:

```bash
monsieurm solve 2025-07-18
```

To view answers:

```bash
monsieurm display
```

You can also provide a date to display results for a past quiz.

> [!WARNING]
> The output of `display` will contain spoilers to the quiz when the LLM gets
> an answer right, so make sure you solved it yourself before running it.

Because human participants aren't allowed to use any help, Mistral is of
course _not_ given any tools or the option to search. This is man vs
machine at its most honest and brutal.

## Formatting and Type Checking

The project uses [Ruff](https://astral.sh/ruff) for formatting:

```bash
uv run ruff check
All checks passed!
```

and [ty](https://docs.astral.sh/ty/) for type checking:

```bash
uv run ty check
All checks passed!
```
