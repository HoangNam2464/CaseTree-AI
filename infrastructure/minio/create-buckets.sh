#!/bin/sh
# Create MinIO buckets for CaseTree AI
# Run this after MinIO starts
# Usage: docker exec casetree_minio sh /create-buckets.sh

mc alias set local http://localhost:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
mc mb local/${MINIO_BUCKET_MATERIALS:-casetree-materials} --ignore-existing
echo "MinIO buckets created successfully"
