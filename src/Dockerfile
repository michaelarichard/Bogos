# 104 MB
#FROM python:3.7.2-alpine

# 117 MB
#FROM python:3.8.2-alpine3.11
FROM python:3.11-slim-bullseye

RUN pip install --upgrade pip

RUN groupadd worker && useradd -rm -d /home/worker -s /bin/bash -g worker -G worker -u 1000 worker
USER worker
WORKDIR /home/worker

COPY --chown=worker:worker requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker . /app

# LABEL maintainer="Your Name <your-mail@example.com>" \
#      version="1.0.0"

ENV FLASK_RUN_PORT 8000

ENV FLASK_APP /app/server.py

ENV FLASK_ENV production

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi", "--chdir", "/app", "--workers=2"]
