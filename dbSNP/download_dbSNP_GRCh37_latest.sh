#!/bin/bash
set -euo pipefail

# Set filenames
DBSNP_FILE="Homo_sapiens.vcf.gz"
INDEX_FILE="${DBSNP_FILE}.tbi"
META_FILE="dbsnp_ensembl_GRCh37_metadata.txt"

# Base URL for Ensembl dbSNP data on GRCh37
BASE_URL="https://ftp.ensembl.org/pub/grch37/release-110/variation/vcf/homo_sapiens"

# Download dbSNP VCF and index for GRCh37 from Ensembl
wget "${BASE_URL}/${DBSNP_FILE}"
wget "${BASE_URL}/${INDEX_FILE}"

# Extract metadata
zgrep '^##' "$DBSNP_FILE" > "$META_FILE"

echo "✔ Ensembl GRCh37 dbSNP (${DBSNP_FILE}) downloaded and metadata written to ${META_FILE}."
