#!/usr/bin/env python3
"""
VCF Filter Modifier Script

This script modifies the FILTER field in a VCF file based on the sample-level
FT (Filter) field. Specifically, it adds 'LowGQ' to the FILTER column if a variant
has an FT tag of 'LowGQ' but the top-level FILTER field is 'PASS' or does not
already contain 'LowGQ'.

It also removes any variants that are not on the primary assembly chromosomes
(i.e., it filters out contigs like ALT, decoy, or random chromosomes).

It also removes the "chr" prefix from chromosomal IDs

Usage:
    python modify_filter_vcf.py <input_dir> <output_dir> sample.vcf

This script can also be imported and used as a module via `run_vcf_filter_modification(...)`.
"""

import sys
import os

# Set of canonical primary chromosome names WITHOUT the 'chr' prefix.
# Includes autosomes 1-22, sex chromosomes X and Y, and mitochondrial chromosomes M and MT.
PRIMARY_CHROMOSOMES = {str(i) for i in range(1, 23)} | {"X", "Y", "M", "MT"}

def run_vcf_filter_modification(input_dir, output_dir, vcf_filename):
    """
    Modify the FILTER field of a VCF file based on sample FT values,
    and write the modified VCF to the output directory.

    Steps:
      - Reads the input VCF file line-by-line.
      - Writes header lines unchanged.
      - For variant lines:
        * Normalizes chromosome name by removing 'chr' prefix if present.
        * Filters out variants not on primary assembly chromosomes.
        * Checks the FORMAT column for 'FT' field and sample FT value.
        * If sample FT is 'LowGQ':
          - If FILTER is 'PASS', replaces it with 'LowGQ'.
          - Else, adds 'LowGQ' to FILTER if not already present.
      - Writes modified variant lines to output file.

    Parameters:
        input_dir (str): Path to directory containing the input VCF file.
        output_dir (str): Path to directory where output will be saved.
        vcf_filename (str): Filename of the VCF to process.

    Returns:
        str: Full path to the modified VCF output file.
    """
    # Construct full path to input VCF file
    input_path = os.path.join(input_dir, vcf_filename)
    # Verify that the input file exists
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Create output directory if it does not already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create the output file name by appending '_modified_filter' before extension
    output_filename = os.path.splitext(vcf_filename)[0] + "_modified_format.vcf"
    output_path = os.path.join(output_dir, output_filename)

    modified_count = 0  # Counter for variants where FILTER field is modified
    total_variants = 0  # Counter for variants processed on primary chromosomes

    # Open input and output files for reading and writing, respectively
    with open(input_path, 'r') as fin, open(output_path, 'w') as fout:
        # Process the VCF file line by line
        for line in fin:
            # If the line is a header line (starts with '#'), write it unchanged
            if line.startswith('#'):
                fout.write(line)
                continue  # Move to the next line

            # Split the variant line by tab to access individual columns
            fields = line.rstrip('\n').split('\t')

            # Extract the chromosome field (column 1)
            chrom_raw = fields[0]

            # Normalize chromosome name by removing the 'chr' prefix if it exists
            # For example, 'chr1' becomes '1' to match PRIMARY_CHROMOSOMES set
            chrom = chrom_raw[3:] if chrom_raw.startswith("chr") else chrom_raw
            fields[0] = chrom

            # Replace X with 23, Y with 34 and M or MT with 25
            if fields[0].upper() == "X":
                fields[0] = "23"
            if fields[0].upper() == "Y":
                fields[0] = "24"
            if fields[0].upper() == "MT":
                fields[0] = "25"
            if fields[0].upper() == "M":
                fields[0] = "25"

            # Skip variants that are not on primary chromosomes
            # This removes alternate contigs, decoys, and other non-primary sequences
            if chrom not in PRIMARY_CHROMOSOMES:
                continue  # Skip this variant line entirely

            total_variants += 1  # Count this variant as processed

            # Extract the FILTER column (7th column, zero-based index 6)
            filter_field = fields[6]
            # Extract the FORMAT column (9th column, index 8) which describes sample fields
            format_field = fields[8]
            # Extract the first sample's data (10th column, index 9)
            sample_field = fields[9]

            # Split the FORMAT string by colon to get the keys (e.g., GT, AD, DP, FT)
            format_keys = format_field.split(':')
            # Split the sample data by colon to get corresponding values for each FORMAT key
            sample_values = sample_field.split(':')

            # Check if 'FT' (Filter tag) exists in the FORMAT keys
            if 'FT' in format_keys:
                # Find the index position of 'FT' in FORMAT keys
                ft_index = format_keys.index('FT')
                # Extract the sample's FT value using the index
                sample_filter = sample_values[ft_index]

                # If the sample-level FT value is 'LowGQ' (Low Genotype Quality)
                if sample_filter == 'LowGQ':
                    if filter_field == 'PASS':
                        # If top-level FILTER is 'PASS', replace it with 'LowGQ'
                        fields[6] = 'LowGQ'
                        modified_count += 1  # Increment modification counter
                    else:
                        # Otherwise, parse FILTER field as semicolon-separated list
                        filters = filter_field.split(';')
                        # Append 'LowGQ' if it is not already present
                        if 'LowGQ' not in filters:
                            filters.append('LowGQ')
                            # Join filters back into a semicolon-separated string
                            fields[6] = ';'.join(filters)
                            modified_count += 1  # Increment modification counter

            # Write the (potentially modified) variant line to output
            fout.write('\t'.join(fields) + '\n')

    # Print summary of processing results
    print(f"Processed {total_variants} variant lines.")
    print(f"Modified FILTER field to include 'LowGQ' in {modified_count} lines.")
    print(f"Output written to: {output_path}")

    # Return output file path for convenience
    return output_path

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
