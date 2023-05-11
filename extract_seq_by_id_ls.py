#!/usr/bin/python3

# extract_seq_by_id_ls.py

# Hsin-Ying Chang <dnx202138@gmail.com>
# v1 2023/01/18

# Usage: python3 /home/xinchang/pyscript_xin/extract_seq_by_id_ls.py --input=/scratch/xinchang/cyano10/cyano10.18/blast_16S/16S.fasta --list=/scratch/xinchang/cyano10/cyano10.18/blast_16S/16S_download.list --output_dir=/scratch/xinchang/cyano10/cyano10.18/output --base_name=16S_extract.fasta --index_in=1 --index_out=0

import argparse
from Bio import SeqIO
import os

def main():
    parser = argparse.ArgumentParser(
            description=("Parse the sequences from fasta by id list"),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--input",
                        type=str,
                        default=None,
                        help="input file.")
    parser.add_argument("--list",
                        type=str,
                        default=None,
                        help="list file.")
    parser.add_argument("--output_dir",
                        type=str,
                        default="./output",
                        help="Directory for output files. Please provide absolute path.")
    parser.add_argument("--base_name",
                        type=str,
                        default="seqout.fasta",
                        help="Base name for output file.")        
    parser.add_argument("--index_in",
                        type=str,
                        default=None,
                        help="id columns.")
    parser.add_argument("--index_out",
                        type=str,
                        default=None,
                        help="run name columns.")

    # Defining variables from input
    args = parser.parse_args()
    input_file = args.input
    list_file = args.list
    in_col = int(args.index_in)
    out_col = int(args.index_out)

    # Create a new directory for sequences output
    if not os.path.exists("%s" % args.output_dir):
        output_dir = os.makedirs("%s" % args.output_dir)
    else:
        output_dir = args.output_dir

    basename = args.base_name
    output_file = os.path.join(output_dir, basename)
    output = open(output_file, "w")

    # Concact the name columns and run name columns
    ids = ids_ls(list_file, in_col, out_col)

    # Count the sequence number
    count_in = 0
    count_out = 0
    # Extract the ids and sequences out to the new file
    for record in SeqIO.parse(input_file, "fasta"):
        count_in += 1
        for i in range(len(ids)):
            if ids[i][0] in record.description:
                ids[i][0] = record.id     
            if ids[i][0] == record.id: 
                count_out += 1
                record.id = ids[i][1]
                output.write(">" + record.id + "\n" + str(record.seq) + "\n")
    print("count_in = " + str(count_in) + "\n" + "count_out = " + str(count_out) + "\n")
    output.close()

def ids_ls(list_file, in_col, out_col):
    ids = []
    with open(list_file) as ls:  
        for line in ls:
            cols = line.split("\t")
            ids.append([cols[in_col], cols[out_col]])
    return ids

if __name__ == '__main__':
    main()