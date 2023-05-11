#!/usr/bin/python3

# concat_seqs.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/04/10

# Usage: python3 /home/xinchang/pyscript/pyscript_xin/concat_seqs.py --in_dir=/scratch/xinchang/cyano11/cyano11.15/TW_strains --ext=".fasta" --seqname="TW" > /scratch/xinchang/cyano11/cyano11.15/seqs/TW.fasta

import argparse
import os, glob


def main():
    parser = argparse.ArgumentParser(
            description=("Concat sequences."),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--in_dir",
                        type=str,
                        default=None,
                        help="Input sequences directory. Please put the seq files into a location and provide the abosolute pathway.")
    parser.add_argument("--ext",
                        type=str,
                        default=".fasta",
                        help="Please provide the extensions of sequence files.")
    parser.add_argument("--seqname",
                        type=str,
                        default=None,
                        help="Please provide a name for concatenated sequence.")

    # Defining variables from inputs
    args = parser.parse_args()
    in_dir = args.in_dir
    name = args.seqname

    # Find input files from specific directory
    inputs = glob.glob(os.path.join(in_dir, "*%s" % args.ext))

    # Parse and concat sequences
    sequences = concat_seq(inputs)

    # Write the sequence into a new fasta
    print(">" + name)
    print(*sequences, sep = "")

def concat_seq(inputs):
    sequences = []
    for in_file in inputs:
        with open(in_file) as seqfile:
            lines = seqfile.read().splitlines()
            i = 0
            while i < len(lines) and lines[i][0] == ">":
                sequences.append(lines[i+1])
                i += 2
    return sequences

if __name__ == '__main__':
    main()
