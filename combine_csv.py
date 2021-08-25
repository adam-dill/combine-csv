#!/usr/bin/python
import os
import sys, getopt
import csv


# the mapping of header names
map = dict({
	'firstName': ['firstName', 'First Name', 'fname', 'first_name'],
	'lastName': ['lastName', 'Last Name', 'lname', 'last_name'],
	'email': ['email', 'Email', 'email'],
	'ssn': ['ssn', 'SSN', 'social'],
	'cin': ['cin', 'CIN']
})


def getColumns():
	out_columns = []
	for key in map:
		out_columns.append(key)
	return out_columns

def processFiles(directory):
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
	return out_data

def writeFile(out_file, out_data):
	out_columns = getColumns()
	try:
		with open(out_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=out_columns)
			writer.writeheader()
			for data in out_data:
				writer.writerow(data)
	except IOError:
		print("I/O error")

def main(argv):
	# the directory to process (optional argument)
	directory = os.getcwd() + "/"
	
	# the output file (optional argument)
	out_file = "output.csv"
	
	# handle the arguments
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
			
	out_columns = getColumns()
	out_data = processFiles(directory)
	writeFile(out_file, out_data)
	

if __name__ == "__main__":
	main(sys.argv[1:])