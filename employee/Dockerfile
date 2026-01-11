FROM python:3.10-slim AS base
WORKDIR /employee

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src
COPY .env .

FROM base AS test
COPY tests/ ./tests

COPY behave.ini .
CMD ["sh", "-c", "python -m behave"]

FROM base AS production
EXPOSE 5000
COPY tests/ ./tests
# Running as a module due to src directory
ENTRYPOINT ["python", "-m", "src.main"]
