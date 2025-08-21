#!/bin/bash
set -euo pipefail

# ---- Settings ----
DBSNP_FILE="GCF_000001405.25"   # core filename (no .vcf.gz)
BASE_URL="https://ftp.ncbi.nih.gov/snp/archive/b154/VCF"

RAW_VCF="${DBSNP_FILE}.vcf.gz"
RAW_META="${DBSNP_FILE}_pre_metadata.txt"

RENAMED_VCF="${DBSNP_FILE}.ucsc.vcf.gz"
RENAMED_META="${DBSNP_FILE}_post_metadata.txt"

# ---- Step 1: Download dbSNP ----
echo "⬇ Downloading dbSNP from NCBI..."
wget -O - "${BASE_URL}/${DBSNP_FILE}" | bgzip -c > "$RAW_VCF"

# ---- Step 2: Extract pre-transformation metadata ----
echo "📝 Extracting pre-transformation metadata..."
zgrep '^##' "$RAW_VCF" > "$RAW_META"

# ---- Step 3: Create rename mapping ----
cat > rename_chrs.txt <<'EOF'
NC_000001.10   chr1
NC_000002.11   chr2
NC_000003.11   chr3
NC_000004.11   chr4
NC_000005.9    chr5
NC_000006.11   chr6
NC_000007.13   chr7
NC_000008.10   chr8
NC_000009.11   chr9
NC_000010.10   chr10
NC_000011.9    chr11
NC_000012.11   chr12
NC_000013.10   chr13
NC_000014.8    chr14
NC_000015.9    chr15
NC_000016.9    chr16
NC_000017.10   chr17
NC_000018.9    chr18
NC_000019.9    chr19
NC_000020.10   chr20
NC_000021.8    chr21
NC_000022.10   chr22
NC_000023.10   chrX
NC_000024.9    chrY
NC_012920.1    chrMT
NC_001807.4    chrM
EOF

# ---- Step 4: Perform renaming ----
echo "🔄 Renaming chromosomes to UCSC-style..."
bcftools annotate --rename-chrs rename_chrs.txt -Oz -o "$RENAMED_VCF" "$RAW_VCF"

# ---- Step 5: Extract post-transformation metadata and clean ----
echo "📝 Extracting post-transformation metadata..."
zgrep '^##' "$RENAMED_VCF" > "$RENAMED_META"
mv GCF_000001405.25.ucsc.vcf.gz Homo_sapiens_assembly19.dbsnplatest.vcf.gz
tabix -p vcf Homo_sapiens_assembly19.dbsnplatest.vcf.gz
mv GCF_000001405.25_post_metadata.txt Homo_sapiens_assembly19.dbsnplatest_metadata.txt
rm GCF_000001405.25*

# ---- Done ----
echo "✔ Downloaded:    $RAW_VCF"
echo "✔ Metadata pre:  $RAW_META"
echo "✔ Renamed VCF:   $RENAMED_VCF"
echo "✔ Metadata post: $RENAMED_META"
