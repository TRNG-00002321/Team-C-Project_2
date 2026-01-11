FROM python:3.10-slim AS base
WORKDIR /employee

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src
COPY .env .

FROM base AS test
COPY tests/ ./tests

COPY behave.ini .

CMD ["sh", "-c", "python -m pytest --alluredir=allure-results; python -m src.main & sleep 10; python -m behave"]

FROM base AS production
EXPOSE 5000
# Running as a module due to src directory
ENTRYPOINT ["python", "-m", "src.main"]
