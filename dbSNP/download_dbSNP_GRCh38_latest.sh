#!/bin/bash
set -euo pipefail

# Set filenames
DBSNP_FILE="GCF_000001405.40.gz"
INDEX_FILE="${DBSNP_FILE}.tbi"
META_FILE="dbsnp_GRCh38_metadata.txt"

# Download dbSNP VCF and index for GRCh38
wget ftp://ftp.ncbi.nih.gov/snp/latest_release/VCF/${DBSNP_FILE}
wget ftp://ftp.ncbi.nih.gov/snp/latest_release/VCF/${INDEX_FILE}

# Extract metadata
zgrep '^##' "$DBSNP_FILE" > "$META_FILE"

echo "✔ GRCh38 dbSNP (${DBSNP_FILE}) downloaded and metadata written to ${META_FILE}."

