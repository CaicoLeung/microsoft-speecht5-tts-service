FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# install system dependencies
RUN apt-get update && apt-get install -y \
  libsndfile1 \
  libsndfile1-dev \
  # Add audio backend dependencies
  alsa-utils \
  libasound2 \
  libasound2-plugins \
  pulseaudio \
  && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project

# Copy the project into the image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "main.py"]
