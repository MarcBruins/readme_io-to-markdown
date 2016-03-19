#! /usr/bin/env python 

import argparse
import json
import csv
import os
import sys
parser = argparse.ArgumentParser(description='')
parser.add_argument('files', type=str, nargs='+',
                    help='files')
args = parser.parse_args()

def parse_json_block(infile, line):
	json_str = ""
	while not "[/block]" in line:
		line = infile.next()
		if not "[/block]" in line:
			json_str += line
	d= json.loads(json_str)	
	return d


f = args.files[0]
for f in args.files:
	with open(f, 'r') as infile:
		file_str = ""
		for line in infile:
			if "--" in line:
				pass
			elif "title:" in line:
				title = line.split(":")[1]
				file_str += "# %s\n\n" % title.replace('"','')
			elif "excerpt:" in line:
				excerpt = line.split(":")[1]
			elif "[block:api-header]" in line:
				d = parse_json_block(infile, line)
				file_str += "## %s\n\n" % d.get("title")
			elif "[block:callout]" in line:
				d = parse_json_block(infile, line)
				file_str += "## ! %s !\n\n" % d.get("title")
				file_str += "\t %s \n\n" % d.get("body")
			elif "[block:code]" in line:
				d = parse_json_block(infile, line)
				for code in d["codes"]:
					file_str += "\t %s \n" % code.get("code").replace("\n", "\n\t")
			else:
				file_str += line+"\n"

	with open(f, 'w') as outfile:
		outfile.write(file_str)
