# Java Manager App Dockerfile
# Multi-stage build for optimized production image

# Build stage
#NOTICE: MUST BE BUILT FROM THE PARENT DIRECTORY
#this is so we can access the db file
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies (cached layer)
COPY manager/pom.xml .
RUN mvn dependency:go-offline -B
#Copy env and db files

COPY manager/.env .
COPY ./test_expense_manager.db /app/test_expense_manager.db

# Copy source code and build

COPY manager/src ./src/
RUN mvn clean package -DskipTests -B

# Production stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -D appuser

# Copy the built JAR from builder stage
COPY --from=builder /app/target/manager-1.0-SNAPSHOT-jar-with-dependencies.jar app.jar

# Create directory for database (shared volume mount point)
RUN mkdir -p /data && chown appuser:appgroup /data

# Switch to non-root user
USER appuser

# Environment variables
ENV JAVA_OPTS="-Xms256m -Xmx512m"
ENV DATABASE_PATH=/app/test_expense_manager.db
# Expose Javalin port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5001/health || exit 1

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]