# Use a lightweight official Python runtime
FROM python:3.10-slim

# Set system environment adjustments
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# REMOVED build-essential to completely skip the heavy 87MB apt download loop.
# Only keeping curl if required for health checks, otherwise you can remove it too.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch==2.12.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir pymilvus==2.4.0 kafka-python-ng==2.2.2 marshmallow==3.20.0 environs==9.5.0 rank_bm25==0.2.2 google-genai && \
    pip install --no-cache-dir -r requirements.txt

# Copy application layers over
COPY . .

# Expose FastAPI server port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]