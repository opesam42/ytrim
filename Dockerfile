# Use an official Python image as a base
FROM python:3.10-slim

# Install dependencies for Playwright and Chromium
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y wget curl gnupg2 ca-certificates libnss3 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /ytrim

# Copy only requirements first to optimize layer caching
COPY requirements.txt /ytrim/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and the required browsers (Chromium, Webkit, Firefox), with system dependencies
RUN python -m pip install playwright && \
    python -m playwright install --with-deps chromium

# Copy the entire Django project into the container
COPY . /ytrim/

# Expose the port the app runs on
EXPOSE 8000

# Use gunicorn for production, or you can use Django's development server for local testing
CMD ["gunicorn", "ytrim.wsgi:application", "--bind", "0.0.0.0:8000"]
