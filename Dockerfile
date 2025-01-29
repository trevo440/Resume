# Use an official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for WeasyPrint
RUN apt-get update && \
    apt-get install -y \
    libgtk-3-0 \
    libcairo2 \
    libpango1.0-0 \
    libjpeg62-turbo-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    curl && \
    # Install Node.js and npm
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    # Clean up to reduce image size
    rm -rf /var/lib/apt/lists/*

# Install OpenAI client using npm
RUN npm install openai --save

# Copy the requirements.txt first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Command to run Flask inside the container
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
