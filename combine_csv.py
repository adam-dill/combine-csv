#!/usr/bin/python
import os
import sys, getopt
import csv

def main(argv):
	# handle the arguments
	directory = os.getcwd() + "/"
	out_file = "output.csv"
	try:
		opts, args = getopt.getopt(argv,"hd:o:",["dir=", "out="])
	except getopt.GetoptError:
		print('combine_csv.py -d <directory> -o <output>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('combine_csv.py -d <directory> -o <output>')
			sys.exit()
		elif opt in ("-d", "--dir"):
			directory = arg
		elif opt in ("-o", "--out"):
			out_file = arg
	
	# the mapping of header names
	map = dict({
		'firstName': ['First Name', 'fname'],
		'lastName': ['Last Name', 'lname'],
		'email': ['Email', 'email'],
		'ssn': ['SSN', 'social']
	})
	
	
	out_columns = []
	for key in map:
		out_columns.append(key)
		
	out_data = []
	files = os.listdir(directory)
	for file in files:
		if file.endswith(".csv"):
			with open(directory + file) as csvfile:
				#reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				reader = csv.DictReader(csvfile)
				
				for row in reader:
					row_data = {}
					for (k, v) in row.items():
						for key in map:
							if k in map[key]:
								row_data[key] = v
					if bool(row_data):
						out_data.append(row_data)
		
	try:
		with open(out_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=out_columns)
			writer.writeheader()
			for data in out_data:
				writer.writerow(data)
	except IOError:
		print("I/O error")
	

if __name__ == "__main__":
	main(sys.argv[1:])