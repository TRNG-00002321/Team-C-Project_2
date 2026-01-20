# Java Manager App Dockerfile
# Multi-stage build for optimized production image

# Build stage
#NOTICE: MUST BE BUILT FROM THE PARENT DIRECTORY
#this is so we can access the db file
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies (cached layer)
COPY manager/.env .
COPY manager/pom.xml .
RUN mvn dependency:go-offline -B
#Copy env and db files


COPY ./expense_manager.db /app/expense_manager.db
COPY ./test_expense_manager.db /app/test_expense_manager.db

# Copy source code and build

COPY manager/src ./src/
RUN mvn clean package -DskipTests -B

# Production stage
FROM eclipse-temurin:17-jdk

WORKDIR /app
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     gnupg \
#     ca-certificates \
#     wait-for-it \
#     && curl -fSsL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
#     && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
#     && curl -fSsL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-edge.gpg \
#     && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-edge.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list \
#     && apt-get update && apt-get install -y --no-install-recommends \
#     google-chrome-stable \
#     firefox \
#     microsoft-edge-stable \
#     && rm -rf /var/lib/apt/lists/*

# RUN apt-get install -y wget
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# RUN apt-get update && apt-get -y install google-chrome-stable
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable
#
# # install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#
# # Create non-root user for security
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -s /bin/bash appuser


# Copy the built JAR from builder stage
COPY --from=builder /app/target/manager-1.0-SNAPSHOT-jar-with-dependencies.jar app.jar

# Create directory for database (shared volume mount point)
RUN mkdir -p /data && chown appuser:appgroup /data
COPY ./expense_manager.db ../data
COPY ./test_expense_manager.db ../data
RUN chown appuser:appgroup /data/expense_manager.db
RUN chown appuser:appgroup /data/test_expense_manager.db
RUN chmod -R 777 /app
# Switch to non-root user
USER appuser

# Environment variables
ENV JAVA_OPTS="-Xms256m -Xmx512m"
ENV BROWSER=chrome \
    DATABASE_PATH=../data/expense_manager.db \
    TEST_DATABASE_PATH=../data/test_expense_manager.db \
    TEST_MODE=true
# Expose Javalin port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5001/health || exit 1

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]