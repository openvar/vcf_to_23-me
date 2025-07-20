#!/bin/bash
set -euo pipefail

# Set filenames
DBSNP_FILE="GCF_000001405.40.gz"
INDEX_FILE="${DBSNP_FILE}.tbi"
META_FILE="dbsnp_GRCh38_metadata.txt"

# Use Broad's Google Cloud bucket (public)
BASE_URL="https://storage.googleapis.com/genomics-public-data/resources/broad/hg38/dbsnp"

# Download dbSNP VCF and index for GRCh38
wget "${BASE_URL}/${DBSNP_FILE}"
wget "${BASE_URL}/${INDEX_FILE}"

# Extract metadata headers
zgrep '^##' "$DBSNP_FILE" > "$META_FILE"

echo "✔ GRCh38 dbSNP (${DBSNP_FILE}) downloaded from Broad bucket and metadata written to ${META_FILE}."
