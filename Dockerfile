#
# Build the application in the `/app` directory using `uv`
#
FROM python:3.13-slim AS builder

# Get the latest `uv` and make it globally executable
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /uvx /bin/

# Recommended by `uv` for prod builds, see docs for details
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# Install dependencies
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy the app itself and install
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

#
# Create an image with the runnable cli tool, but without `uv`
#
FROM python:3.13-slim

# Setup a non-root user
RUN groupadd --system --gid 999 monsieur \
    && useradd --system --gid 999 --uid 999 --create-home monsieur

# Copy the application from the builder
COPY --from=builder --chown=monsieur:monsieur /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the non-root user to run our application
USER monsieur

# Use `/app` as the working directory
WORKDIR /app

# Add entrypoint
ENTRYPOINT ["monsieurm"]
CMD ["display"]
