# Pull official base image
FROM python:3.12.4-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# # Install system dependencies and build tools
RUN apt-get update && \
    apt-get install -y \
    docker.io

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .
COPY build_ccextractor_image.sh /build_ccextractor_image.sh
RUN chmod +x /build_ccextractor_image.sh

