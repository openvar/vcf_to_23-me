import sys
import pysam

def filter_and_add_rsids(input_vcf, dbsnp_vcf, output_vcf):
    """
    Adds rsIDs to variants in input_vcf using dbsnp_vcf. Outputs to output_vcf.
    Prints debug info when an rsID is found.
    """
    dbsnp = pysam.VariantFile(dbsnp_vcf)         # bgzipped + indexed dbSNP
    infile = pysam.VariantFile(input_vcf)        # input can be plain or bgzipped
    outfile = pysam.VariantFile(output_vcf, "w", header=infile.header)

    kept, updated, dropped = 0, 0, 0

    for rec in infile.fetch():
        if rec.id not in (None, "."):
            # This is a real rsID
            outfile.write(rec)
            kept += 1
            continue

        found = False
        # fetch 1-base window in dbSNP (0-based start, end exclusive)
        for dbsnp_rec in dbsnp.fetch(rec.chrom, rec.pos - 1, rec.pos):
            # match reference allele
            if dbsnp_rec.ref == rec.ref:
                # match any ALT allele
                for alt in rec.alts:
                    if alt in dbsnp_rec.alts:
                        rec.id = dbsnp_rec.id  # add rsID
                        outfile.write(rec)
                        updated += 1
                        found = True
                        break
                if found:
                    break

        if not found:
            dropped += 1

    infile.close()
    outfile.close()
    dbsnp.close()

    print(f"[check_rsIDs.py] Kept {kept} existing rsIDs.")
    print(f"[check_rsIDs.py] Added {updated} rsIDs from dbSNP.")
    print(f"[check_rsIDs.py] Removed {dropped} variants with no rsID.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python check_rsIDs.py <input.vcf[.gz]> <dbsnp.vcf.gz> <output.vcf[.gz]>")
        sys.exit(1)

    input_vcf = sys.argv[1]
    dbsnp_vcf = sys.argv[2]
    output_vcf = sys.argv[3]

    filter_and_add_rsids(input_vcf, dbsnp_vcf, output_vcf)

# <LICENSE>
# Copyright (C) 2016-2025 VariantValidator Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# </LICENSE>
