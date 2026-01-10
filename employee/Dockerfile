FROM python:3.10-slim

WORKDIR /employee

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tests/ ./tests
COPY src/ ./src

EXPOSE 5000
# Running as a module due to src directory
CMD ["python", "-m", "src.main"]
