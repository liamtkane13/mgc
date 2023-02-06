#!/usr/bin/env python3

import argparse
from Bio.Seq import Seq
From Bio.Alphabet import IUPAC

parser = argparse.ArgumentParser(description='Enter a Protein Sequence to be converted into a DNA Sequence.')
parser.add_argument('-s', '--seq', help='Protein Sequence to convert', required=True, dest='seq')
args = parser.parse_args()

def 
