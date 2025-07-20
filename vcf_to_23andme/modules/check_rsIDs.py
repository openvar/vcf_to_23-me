#!/usr/bin/env python3

"""
check_rsIDs.py

For each variant in the input VCF:
- If it has an rsID, keep it.
- If it doesn't, try to look up an rsID from a dbSNP VCF.
- If no rsID is found, discard the variant.

Usage:
    python check_rsIDs.py <input_vcf> <dbsnp_vcf.gz> <output_vcf>
"""

import sys
import pysam

def filter_and_add_rsids(input_vcf, dbsnp_vcf, output_vcf):
    """
    Adds rsIDs to variants in input_vcf using dbsnp_vcf. Outputs to output_vcf.

    Parameters:
    - input_vcf (str): Path to the VCF to be cleaned.
    - dbsnp_vcf (str): Path to bgzipped + indexed dbSNP VCF.
    - output_vcf (str): Path to write the updated VCF.
    """
    dbsnp = pysam.VariantFile(dbsnp_vcf)
    input_file = open(input_vcf)
    output_file = open(output_vcf, 'w')

    kept, updated, dropped = 0, 0, 0

    for line in input_file:
        if line.startswith('#'):
            output_file.write(line)
            continue

        fields = line.strip().split('\t')
        chrom, pos, id_field, ref, alt = fields[0], int(fields[1]), fields[2], fields[3], fields[4]

        if id_field != ".":
            output_file.write(line)
            kept += 1
            continue

        # Attempt rsID lookup from dbSNP VCF
        found = False
        for rec in dbsnp.fetch(chrom, pos - 1, pos):
            if rec.pos == pos and rec.ref == ref and alt in rec.alts:
                fields[2] = rec.id  # Add the rsID
                output_file.write('\t'.join(fields) + '\n')
                updated += 1
                found = True
                break

        if not found:
            dropped += 1

    input_file.close()
    output_file.close()
    print(f"[check_rsIDs.py] Kept {kept} existing rsIDs.")
    print(f"[check_rsIDs.py] Added {updated} rsIDs from dbSNP.")
    print(f"[check_rsIDs.py] Removed {dropped} variants with no rsID.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python check_rsIDs.py <input_vcf> <dbsnp_vcf.gz> <output_vcf>")
        sys.exit(1)

    input_vcf = sys.argv[1]
    dbsnp_vcf = sys.argv[2]
    output_vcf = sys.argv[3]

    filter_and_add_rsids(input_vcf, dbsnp_vcf, output_vcf)
