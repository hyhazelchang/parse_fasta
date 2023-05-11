#!/usr/bin/python3

# get_gap_from_map.py

# Hsin-Ying Chang <dnx202138@gmail.com>
# v1 2023/02/22

# Usage: python3 /home/xinchang/pyscript/pyscript_xin/get_gap_from_map.py --input="/scratch/xinchang/cyano19/cyano19.02/bwa_00_05/cyano19.02.02.bed" --seq_name=cyano19.2.01 --seq_len=26120825 > /scratch/xinchang/cyano19/cyano19.02/fill.07.gap

# if the system can't be installed the pandas module, get pip installer under user by this cmd: wget https://bootstrap.pypa.io/pip/3.6/get-pip.py (according to diiferent version of your python, this one is 3.6)
# then install pip under the user: python get-pip.py --user
# after installing pip, use pip to install pandas under the user. so go to the bin: cd .local/bin; ./pip install pandas --user

import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
            description=("Get the gaps from alignment between velvet contigs and reference genome"),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--input",
                        type=str,
                        default=None,
                        help="input file (bed file). Please give the absolute path.")
    parser.add_argument("--seq_name",
                        type=str,
                        default=None,
                        help="sequence name")
    parser.add_argument("--seq_len",
                        type=str,
                        default=None,
                        help="sequence length")           

    # Defining variables from input
    args = parser.parse_args()
    in_file = args.input
    name = args.seq_name
    length = args.seq_len

    # Read the bed file into dataframe
    df = pd.read_csv(in_file, header = None, sep = "\t")

    # delete the repeat rows from top to bottom
    up, down = 0, 1
    while down < len(df.index):
        if df.iloc[up, 1] <= df.iloc[down, 1] and df.iloc[down, 1] < df.iloc[up, 2] and df.iloc[up, 1] < df.iloc[down, 2] and df.iloc[down, 2] < df.iloc[up, 2]:
            df.drop(df.index[down], inplace = True, errors = "raise")
            df = df.reset_index(drop = True)
        else:
            up = down
            down += 1

    # delete the repeat rows from bottom to top
    up, down = len(df.index)-2, len(df.index)-1
    while up >= 0:
        if df.iloc[down, 1] <= df.iloc[up, 1] and df.iloc[up, 1] < df.iloc[down, 2] and df.iloc[down, 1] < df.iloc[up, 2] and df.iloc[up, 2] < df.iloc[down, 2]:
            df.drop(df.index[up], inplace = True, errors = "raise")
            df = df.reset_index(drop = True)
        else:
            down = up
            up -= 1

    # create short Ns
    sNs = ""
    for i in range(200):
        sNs += "N"

    # create short Ns
    lNs = ""
    for i in range(500):
        lNs += "N"

    # create a list for creating the Ns gap for further re-sequencing
    for nrow in range(1, len(df.index)-1):
        if df.iloc[nrow, 1] <= df.iloc[nrow-1, 2] and df.iloc[nrow, 2] > df.iloc[nrow-1, 2]:
            print(name + "\t" + length + "\t" + str(1) + "\t" + str(df.iloc[nrow-1, 2]) + "\t" + str(df.iloc[nrow-1, 2]) + "\t" + str(200) + "\tY\tM\t" + sNs)
        elif df.iloc[nrow, 1] > df.iloc[nrow-1, 2]:
            print(name + "\t" + length + "\t" + str(1) + "\t" + str(df.iloc[nrow-1, 2]) + "\t" + str(df.iloc[nrow, 1]) + "\t" + str(500) + "\tY\tM\t" + lNs)

if __name__ == '__main__':
    main()