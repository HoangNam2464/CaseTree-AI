#!/bin/sh
# CaseTree AI — Start local infrastructure services
# Usage: sh scripts/development/start-infra.sh
docker compose up -d postgres redis minio
echo "Infrastructure services started."
echo "  PostgreSQL: localhost:5432"
echo "  Redis: localhost:6379"
echo "  MinIO: localhost:9000 (console: localhost:9001)"
