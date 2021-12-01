#!/usr/bin/perl

use strict;
use warnings;
use FileHandle;

MAIN: {
    my $input = $ARGV[0];
    my $fh_IN = new FileHandle;
    my %counts;
    $fh_IN->open($input) || die "ERROR can't open input file\n";
    while(<$fh_IN>) {
	chomp $_;
	my $i = $_;
	my @i = split(/\t/, $i);
	my ($chr, $ref, $var, $gt) = @i;
	my @all_alleles = split(/\,/, $var);
	unshift @all_alleles, $ref;

	my @gt = split(/\//, $gt);
	my $alleles = $all_alleles[$gt[0]] . '/' . $all_alleles[$gt[1]];

	my $variant_type;
	if ($gt eq '0/0') {
	    $variant_type = 'homozygous ref'; #should not see this for this test data set.
	} elsif ($gt eq '1/1') {
	    $variant_type = 'homozygous non-ref';
	} elsif ($gt eq '0/1') {
	    $variant_type = 'heterozygous';
	} elsif ($gt eq '1/2') {
	    $variant_type = 'heterozygous non-ref';
	} else {
	    $variant_type = 'other'; #should not see this for this test data set.
	}
	$counts{$alleles}{$variant_type}++;
    }
    for my $alleles (keys %counts) {
	for my $variant_type (keys %{$counts{$alleles}}) {
	    my $total = $counts{$alleles}{$variant_type};
	    print $variant_type, "\t", $alleles, "\t", $total, "\n";
	}
    }
}
