#!/usr/bin/env python3

import os
import argparse
import subprocess
import logging


def count_total(args):
	view_cmd = ['samtools', 'view', args.bam]
	count_cmd = ['wc', '-l']
	view = subprocess.Popen(view_cmd, stdout=subprocess.PIPE)
	lines = subprocess.check_output(count_cmd, stdin=view.stdout)
	count = float(lines.decode())
	return count

def tss_coverage(args):
	multicov_cmd = ['bedtools', 'multicov', '-bed', args.tss, '-bams', args.bam]
	filter_cmd = ['awk', '{{c+=$NF}} END{{print c}}']
	cover = subprocess.Popen(multicov_cmd, stdout=subprocess.PIPE)
	total = subprocess.check_output(filter_cmd, stdin=cover.stdout)
	count = float(total.decode())
	return count

def main(args):
	logging.info('Starting up.')
	
	total = count_total(args)
	tss = tss_coverage(args)
	
	out_file = os.path.basename(args.bam) + '.FRoT.txt'
	with open(out_file, 'w') as f:
		print('{}\t{}\t{}\t{}'.format(args.bam, tss, total, tss/total), file=f)

	logging.info('Finishing up.')
	return

def process_args():
	parser = argparse.ArgumentParser(description='Insert a useful description here')
	io_group = parser.add_argument_group('I/O arguments')
	io_group.add_argument('--bam', required=True, type=str, help='BAM file to calculate coverage')
	io_group.add_argument('--tss', required=False, type=str, default='hg19_gencode_tss_unique.1kb.bed', help='Path to TSS file')
	return parser.parse_args()

if __name__ == '__main__':
	logging.basicConfig(format='[%(filename)s] %(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M:%S', level=logging.DEBUG)
	args = process_args()
	main(args)
