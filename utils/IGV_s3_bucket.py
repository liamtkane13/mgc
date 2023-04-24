#!/usr/bin/env python3

# IGV_s3_bucket.py

# This is a helper script for the make_IGV_links.nf workflow

import random
import string

def return_random_string():
	s = string.ascii_lowercase+string.digits
	new_string = (''.join(random.sample(s, 6)))
	new_string.rstrip(' ')
	print(new_string)


def main():
	return_random_string()

if __name__ == '__main__':
	main()	