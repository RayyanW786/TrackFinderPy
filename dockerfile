FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg curl build-essential pkg-config libssl-dev \
  && rm -rf /var/lib/apt/lists/*

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/rust/trackfinder-py
RUN pip install maturin && maturin build --release && \
    pip install --no-cache-dir target/wheels/*.whl

WORKDIR /app

ENV UVICORN_HOST=0.0.0.0 UVICORN_PORT=8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
