#!/usr/bin/env python3
"""
Main Script to Trigger VCF Filter Modification, Hard Filtering, and rsID Checking

This script acts as an entry point to run three sequential VCF processing steps:

1. Modify the FILTER field based on sample-level FT (Filter) values and chromosome filtering.
2. Remove all variants that do not have 'PASS' in the FILTER column (hard filter).
3. Add missing rsIDs from a dbSNP VCF or remove variants lacking rsIDs.

It is intended for integration into larger pipelines where multiple
steps/processes are chained together.

Usage:
    python main.py <input_dir> <output_dir> <genome_build> sample.vcf

Arguments:
    input_dir    - Directory containing the original input VCF file.
    output_dir   - Directory where filtered VCF files will be written.
    genome_build - Genome build version, must be either 'GRCh37' or 'GRCh38'.
    sample.vcf   - Filename of the input VCF to process.

This script:
  - Validates command-line arguments including genome build.
  - Calls the VCF modification function.
  - Calls the hard filter function on the modified VCF.
  - Calls the rsID checking and adding function using dbSNP VCF.
  - Handles errors gracefully with informative messages.
  - Prints confirmation messages for pipeline logging.
"""

import sys
import os
from modules import update_formatting, hard_filter
from modules import check_rsIDs  # Assuming check_rsIDs.py is inside modules

def main():
    """
    Main function to execute VCF processing steps sequentially.

    Designed for use in pipelines or workflow managers.
    """
    # --- Step 1: Validate command-line arguments ---
    if len(sys.argv) != 5:
        print(f"Usage: python {sys.argv[0]} <input_dir> <output_dir> <genome_build> sample.vcf")
        print("genome_build must be either 'GRCh37' or 'GRCh38'")
        sys.exit(1)

    # --- Step 2: Parse command-line arguments ---
    input_dir = sys.argv[1]      # Directory with the original input VCF
    output_dir = sys.argv[2]     # Directory to store output files
    genome_build = sys.argv[3].strip()
    vcf_filename = sys.argv[4]   # Input VCF filename

    # Validate genome build
    if genome_build not in ("GRCh37", "GRCh38"):
        print(f"Error: genome_build must be 'GRCh37' or 'GRCh38', got '{genome_build}'")
        sys.exit(1)

    # Extract sample name without extension for consistent naming
    sample_name = os.path.splitext(vcf_filename)[0]

    try:
        # --- Step 3: Run initial VCF filter modification ---
        modified_vcf_path = update_formatting.run_vcf_filter_modification(
            input_dir, output_dir, vcf_filename
        )
        print("Step 1 complete: VCF filter modification finished.")
        print(f"Modified VCF file written to: {modified_vcf_path}")

        # --- Step 4: Run hard filtering on the modified VCF ---
        hardfiltered_vcf_path = hard_filter.run_hard_filter(modified_vcf_path)
        print("Step 2 complete: Hard filtering finished.")
        print(f"Hardfiltered VCF file written to: {hardfiltered_vcf_path}")

        # --- Step 5: Add/check rsIDs using dbSNP VCF (RefSeq style) ---
        # dbSNP files are assumed to live in a parallel dbSNP folder replacing 'vcf' in input_dir
        dbsnp_dir = input_dir.replace(os.sep + "vcf", os.sep + "dbSNP")

        # Select RefSeq dbSNP filename based on genome build
        if genome_build == "GRCh37":
            dbsnp_filename = "GCF_000001405.25.gz"  # dbSNP for GRCh37
        else:  # GRCh38
            dbsnp_filename = "GCF_000001405.39.gz"  # dbSNP for GRCh38

        dbsnp_vcf = os.path.join(dbsnp_dir, dbsnp_filename)

        if not os.path.isfile(dbsnp_vcf):
            raise FileNotFoundError(f"dbSNP VCF not found at expected location: {dbsnp_vcf}")

        rsid_checked_vcf_path = os.path.join(output_dir, f"{sample_name}.rsid_checked.vcf")
        print(f"Step 3: Adding/checking rsIDs from dbSNP file: {dbsnp_vcf}")
        check_rsIDs.filter_and_add_rsids(hardfiltered_vcf_path, dbsnp_vcf, rsid_checked_vcf_path)
        print("Step 3 complete: rsID checking and addition finished.")
        print(f"Final output VCF with rsIDs: {rsid_checked_vcf_path}")

        # Pipeline complete - you can add more steps here if needed

    except Exception as e:
        print(f"Pipeline error: {e}")
        sys.exit(1)  # Return non-zero exit code to indicate failure

if __name__ == "__main__":
    main()

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
