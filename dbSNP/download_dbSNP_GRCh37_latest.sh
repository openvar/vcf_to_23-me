#!/bin/bash
set -euo pipefail

# Set filenames
DBSNP_FILE="GCF_000001405.25.gz"
INDEX_FILE="${DBSNP_FILE}.tbi"
META_FILE="dbsnp_GRCh37_metadata.txt"

# Download dbSNP VCF and index for GRCh37
wget ftp://ftp.ncbi.nih.gov/snp/latest_release/VCF/${DBSNP_FILE}
wget ftp://ftp.ncbi.nih.gov/snp/latest_release/VCF/${INDEX_FILE}

# Extract metadata
zgrep '^##' "$DBSNP_FILE" > "$META_FILE"

echo "✔ GRCh37 dbSNP (${DBSNP_FILE}) downloaded and metadata written to ${META_FILE}."
