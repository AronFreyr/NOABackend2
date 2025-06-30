# syntax=docker/dockerfile:1

ARG PYTHON3_VERSION=13
ARG DEBIAN_VERSION=bookworm
ARG POSTGRES_VERSION=17
ARG PROJECT=NOABackend1
ARG USERNAME=django
ARG USER_UID=1000
ARG USER_GID=$USER_UID

### Base image
FROM ghcr.io/astral-sh/uv:python3.${PYTHON3_VERSION}-${DEBIAN_VERSION}-slim AS base
# Build arguments
ARG POSTGRES_VERSION
ARG USERNAME
ARG USER_UID
ARG USER_GID
# Environment
ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
WORKDIR /app
# Add PostgreSQL repository and its key
RUN apt-get update && apt-get install -y wget gnupg && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
# Install packages including PostgreSQL client
RUN apt-get update && apt-get install -y \
    locales \
    postgresql-client-${POSTGRES_VERSION} \
    && apt-get --purge autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*
COPY gunicorn.conf.py /etc/gunicorn/gunicorn.conf.py
# Create venv
RUN uv venv /opt/venv
# install dependencies
COPY DjangoDadJokes/requirements.txt requirements.txt
RUN uv pip install -r requirements.txt
# Create user, app directories and set permissions
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID --create-home $USERNAME \
    && mkdir -p /app /var/www/static /var/www/media \
    && chown -R $USER_UID:$USER_GID /app /var/www/static /var/www/media /opt/venv

### Development image
FROM base AS dev
RUN apt update && apt install -y --no-install-recommends \
    sudo \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*
USER $USERNAME
EXPOSE 8000

### Production image
FROM base AS prod
ARG SOURCE_COMMIT
ARG PROJECT
ENV SENTRY_RELEASE=$SOURCE_COMMIT
COPY --chmod=755 .circleci/wait-for-postgres.sh /circleci/
COPY ./${PROJECT} /app
USER $USERNAME
CMD ["gunicorn", "--env", "SCRIPT_NAME=/api", "--bind", "0.0.0.0:8000", "-c", "/etc/gunicorn/gunicorn.conf.py", "boilerplate.asgi:application"]
