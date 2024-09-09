#!/bin/bash

# Build the CCExtractor Docker image
docker build -t ccextractor:latest -f Dockerfile.ccextractor .

# Verify the image was created
docker images | grep ccextractor

# Test the CCExtractor image
docker run --rm ccextractor:latest --version
