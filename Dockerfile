# Use an official Python image as a base
FROM python:3.10-slim

# Install dependencies for Playwright and Chromium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg2 \
    ca-certificates \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libx11-xcb1 \
    # Additional dependencies for Playwright
    libxfixes3 \
    libxkbcommon0 \
    libcairo2 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libpangocairo-1.0-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libxrandr2 \
    libgbm1 \
    libxdamage1 \
    # Add missing libraries for Playwright and Chromium
    libXcursor1 \
    libgtk-3-0 \
    libgdk-3-0 \
    libcairo-gobject2 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /ytrim

# Copy only requirements first to optimize layer caching
COPY requirements.txt /ytrim/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and the required browsers (Chromium, Webkit, Firefox)
RUN python -m pip install playwright && \
    python -m playwright install

# Debug: List the contents of the Playwright cache folder
RUN ls -l /ytrim/.cache/ms-playwright

# Copy the entire Django project into the container
COPY . /ytrim/

# Expose the port the app runs on
EXPOSE 8000

# Use gunicorn for production, or you can use Django's development server for local testing
CMD ["gunicorn", "ytrim.wsgi:application", "--bind", "0.0.0.0:8000"]
