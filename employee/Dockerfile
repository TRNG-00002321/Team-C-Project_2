FROM python:3.10-slim AS base
WORKDIR /employee

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src
COPY .env ./

FROM base AS test
COPY tests/ ./tests
ENV TEST_MODE=true

RUN pytest --alluredir=allure-results
COPY behave.ini .
RUN python -m src.main & sleep 5 
RUN behave

FROM base AS production
ENV TEST_MODE=false
EXPOSE 5000
# Running as a module due to src directory
CMD ["python", "-m", "src.main"]
