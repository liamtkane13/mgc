#!/usr/bin/perl

use strict;
use warnings;
use FileHandle;
use Getopt::Long;
use Pod::Usage;

MAIN_CODE: {
	if(scalar @ARGV == 0) { pod2usage(); }

    my $opt = {'assembly' => undef,
			   'label' => undef,
			   'skip_gap' => undef};

	$opt->{'label'} = "HiC_scaffold";

    GetOptions($opt,
	           'assembly=s',
	           'label=s',
	           'skip_gap+') ||  pod2usage();

    my $rh_contigs = parse_contigs($opt->{'assembly'});
    my $fh_IN = new FileHandle;
    $fh_IN->open($opt->{'assembly'}) || die "ERROR: Cannot open assembly file for reading\n";
    my $scaffold_counter = 0;
    while(<$fh_IN>) {
		chomp $_;
		my $i = $_;
		if ($i !~ /^\>/) {
			$scaffold_counter++;
			my $scaffold_name = $opt->{'label'} . '_' . $scaffold_counter;
			my @i = split(/ /, $i);
			foreach my $j (@i) {
				my $strand = '+';
				if ($j < 0) {
					$strand = '-';
				}
				$j = abs($j);
				my $contig_name   = $rh_contigs->{$j}{'contig'};
				my $contig_length = $rh_contigs->{$j}{'length'};
				my @print_me = ($scaffold_name, $contig_name, $strand, $contig_length);
				if ($opt->{'skip_gap'} && $contig_name =~ /^hic_gap_/) {
					next;
				}
				print join("\t", @print_me), "\n";
			}
		}
	}
	$fh_IN->close();
}

sub parse_contigs {
	my $assembly = shift;
	my $fh_IN = new FileHandle;
	$fh_IN->open($assembly) || die "ERROR: Cannot open assembly file for reading\n";
	my %return_me;
	while(<$fh_IN>) {
		chomp $_;
		my $i = $_;
		if ($i =~ /^\>/) {
			$i =~ s/^\>//;
			my @i = split(/ /, $i);
			$return_me{$i[1]}{'contig'} = $i[0];
			$return_me{$i[1]}{'length'} = $i[2];
		}
	}
	$fh_IN->close();
	return \%return_me;
}

=head1 SYNOPSIS

3d-dna-contig-to-scaffold-tsv.pl -assembly *OPTIONAL* -label -skip_gap
