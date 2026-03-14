FROM python:3.11-slim

WORKDIR /app

# Copy shared packages and install them
COPY packages/shared-schemas /packages/shared-schemas
COPY packages/shared-config /packages/shared-config
COPY packages/shared-logging /packages/shared-logging
RUN pip install --no-cache-dir \
    /packages/shared-schemas \
    /packages/shared-config \
    /packages/shared-logging

# Copy and install the service
COPY apps/backend/embedding-service /app
RUN pip install --no-cache-dir .

EXPOSE 8003

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003"]
