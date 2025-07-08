FROM python:3.11-slim
WORKDIR /RAGModel

# Install system dependencies for Rust and package builds
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libffi-dev \
    libssl-dev \
    pkg-config \
    rustc \
    && rm -rf /var/lib/apt/lists/*

COPY . /RAGModel

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "./RAGModel.py"]
