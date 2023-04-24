#!/usr/bin/env python3

# IGV_s3_bucket.py

# This is a helper script for the make_IGV_links.nf workflow

import random
import string

def return_random_string():
	s = string.ascii_lowercase+string.digits
	print(''.join(random.sample(s, 6)))

def main():
	return_random_string()

if __name__ == '__main__':
	main()	