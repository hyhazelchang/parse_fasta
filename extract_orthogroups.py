#!/usr/bin/python3

# extract_orthogroups.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/04/11

# Usage: python3 /home/xinchang/pyscript/pyscript_xin/extract_orthogroups.py --input=/scratch/xinchang/cyano11/cyano11.15/TW+.txt --output=/scratch/xinchang/cyano11/cyano11.15/TW+_group.txt

import argparse


def main():
    parser = argparse.ArgumentParser(
            description=("Concat sequences."),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--input",
                        type=str,
                        default=None,
                        help="Please provide the abosolute pathway.")
    parser.add_argument("--output",
                        type=str,
                        default=None,
                        help="Please provide the abosolute pathway.")


    # Defining variables from inputs
    args = parser.parse_args()
    input = args.input
    output = args.output
    
    # Paese the lines into a group list
    orthogroups = [line.rstrip("\n") for line in open(input)]
    for i in range(len(orthogroups)):
        orthogroups[i] = orthogroups[i].split("\t")
    
    # Append orthogroup representative into list
    ortholist = []
    up, down = 0, 1
    while down < len(orthogroups):
        if orthogroups[up][0] == orthogroups[down][0]:
            down += 1
        else:
            ortholist.append(orthogroups[up])
            up = down

    # Append the last line into list
    ortholist.append(orthogroups[up])

    with open(output, "w") as outlist:
        for line in ortholist:
            outlist.write("\t".join(line) + "\n")
    outlist.close()

if __name__ == '__main__':
    main()