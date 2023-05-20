FROM python:3.11-alpine as requirements-stage

ENV VERSION 1.0.0
 
WORKDIR /tmp

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /tmp/
 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
 
FROM python:3.11-alpine

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN apk add --no-cache libffi openssl && \
    pip install --no-cache-dir --upgrade -r /app/requirements.txt && \
    rm -rf /root/.cache && \
    rm -rf /var/cache/apk/*

COPY ./app /app/

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

USER appuser

WORKDIR /app
 
# Expose the port the app runs in
EXPOSE 1883

# During debugging, this entry point will be overridden. 
CMD ["python", "main.py"]