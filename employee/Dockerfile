FROM python:3.10-slim AS base
WORKDIR /employee

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src
COPY .env .

FROM base AS test
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates \
    && curl -fSsL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && curl -fSsL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-edge.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-edge.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    google-chrome-stable \
    firefox-esr \
    microsoft-edge-stable \
    && rm -rf /var/lib/apt/lists/*

COPY tests/ ./tests
COPY behave.ini .
RUN mkdir -p logs test-results allure-results



FROM base AS production
EXPOSE 5000
COPY tests/ ./tests
ENTRYPOINT ["python", "-m", "src.main"]
