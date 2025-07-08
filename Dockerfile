# =================== STAGE 1: Build ====================
FROM python:3.11-slim as builder

WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libglib2.0-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --user -r requirements.txt

# =================== STAGE 2: Run ====================
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "RAGModel:app"]
