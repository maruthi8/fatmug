#!/bin/bash

# Build and start Docker Compose services
echo "Starting Docker Compose services..."
docker compose up --build --force-recreate --remove-orphans