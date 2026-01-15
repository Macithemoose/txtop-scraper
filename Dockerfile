# Multi-arch (arm64 for Apple Silicon, amd64 for Intel)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps: Chromium + driver + fonts (CJK for robust text), tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    fonts-liberation \
    fonts-noto \
    fonts-noto-cjk \
    ca-certificates \
    curl \
    dumb-init \
  && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN useradd -ms /bin/bash appuser
WORKDIR /app

# Python deps first (layer cache)
COPY requirements.txt .
RUN pip install -r requirements.txt

# App code
COPY . .

# Tell your code where Chromium & chromedriver live
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER=/usr/bin/chromedriver

# Headless flags (can tweak via docker run -e)
ENV SELENIUM_FLAGS="--no-sandbox --disable-dev-shm-usage --disable-gpu --window-size=1366,768"

# Create output dir
RUN mkdir -p /app/data && chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["/usr/bin/dumb-init","--"]
# your main script is main.py
CMD ["python","main.py"]
