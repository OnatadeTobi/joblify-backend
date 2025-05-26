FROM python:3.11-slim

# Install system dependencies required for Playwright and general use
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libgbm1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy entire project
COPY . .

# Collect static files (even if not used yet)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Copy entrypoint script
COPY entrypoint.sh .

# Make it executable (optional if done already)
RUN chmod +x entrypoint.sh

# Run entrypoint script
CMD ["./entrypoint.sh"]
