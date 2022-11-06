# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11-slim as production

RUN useradd zerolab --create-home -u 1000 && mkdir /app /venv && chown -R zerolab /app /venv

WORKDIR /app

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    git \
    postgresql-client \
 && apt-get autoremove && rm -rf /var/lib/apt/lists/*


ENV DJANGO_SETTINGS_MODULE=zerolab.settings \
    GUNICORN_CMD_ARGS="-c gunicorn-conf.py --max-requests 1200 --max-requests-jitter 50 --access-logfile -" \
    PATH=/venv/bin:$PATH \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv \
    WEB_CONCURRENCY=3

EXPOSE 8000

USER zerolab

# Install dependencies
RUN python -m venv /venv
COPY --chown=zerolab requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY --chown=zerolab ./static ./static
COPY --chown=zerolab ./zerolab ./zerolab
COPY --chown=zerolab ./gunicorn-conf.py ./gunicorn-conf.py
COPY --chown=zerolab ./manage.py ./manage.py

RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

CMD set -xe; python manage.py migrate --noinput; gunicorn zerolab.wsgi:application

# Dev
FROM production as dev

USER zerolab

COPY --chown=zeorlab ./requirements-dev.txt ./requirements-dev.txt

RUN pip install -r requirements-dev.txt
