#!/usr/bin/env python3
"""
Hard Filter Module for VCF Files

This module removes all variants that do not have 'PASS' in the FILTER field
from a VCF file. It reads an input VCF (usually the output from a prior filtering
step), filters variants by FILTER status, and writes a new VCF file.

Filename conventions:
  Input: typically the output from the previous step, e.g. sample_modified_format.vcf
  Output: sample_hardfiltered.vcf (placed in the same output directory)

Functions:
  - run_hard_filter(input_vcf_path: str) -> str

Usage:
  Import the module and call `run_hard_filter` with the path to the input VCF.

Example:
  output_path = run_hard_filter("/path/to/sample_modified_format.vcf")

Returns:
  The full path to the hardfiltered output VCF file.
"""

import os

def run_hard_filter(input_vcf_path):
    """
    Filter variants in a VCF file to retain only those with FILTER == 'PASS'.

    Parameters:
        input_vcf_path (str): Full path to the input VCF file.

    Returns:
        str: Full path to the output hardfiltered VCF file.
    """

    # Verify input file exists
    if not os.path.isfile(input_vcf_path):
        raise FileNotFoundError(f"Input VCF file not found: {input_vcf_path}")

    # Prepare output file path by replacing extension and adding suffix
    dirname = os.path.dirname(input_vcf_path)
    basename = os.path.basename(input_vcf_path)
    root, ext = os.path.splitext(basename)

    # Create output filename with '_hardfiltered.vcf' suffix
    output_filename = f"{root}_hardfiltered.vcf"
    output_path = os.path.join(dirname, output_filename)

    # Counters for reporting
    total_variants = 0
    passed_variants = 0

    # Open input and output files
    with open(input_vcf_path, 'r') as fin, open(output_path, 'w') as fout:
        for line in fin:
            # Write header lines unchanged
            if line.startswith('#'):
                fout.write(line)
                continue

            total_variants += 1

            fields = line.rstrip('\n').split('\t')
            filter_field = fields[6]

            # Only write variants with FILTER == 'PASS'
            if filter_field == 'PASS':
                fout.write(line)
                passed_variants += 1
            # Else variant is filtered out (excluded)

    print(f"Total variants processed: {total_variants}")
    print(f"Variants passed FILTER='PASS': {passed_variants}")
    print(f"Filtered VCF written to: {output_path}")

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