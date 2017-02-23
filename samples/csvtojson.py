import csv
import json
import sys

if len(sys.argv) != 3:
	print('Supply input and output names.')
	sys.exit()

csvfile = open(sys.argv[1], 'r')
jsonfile = open(sys.argv[2], 'w')
csv.register_dialect('market', delimiter=';', quoting=csv.QUOTE_NONE)
fieldnames = ("Date","OPEN","HIGH","LOW", "Close", "NUMBER_TICKS", "VOLUME", "VALUE")
reader = csv.DictReader( csvfile, fieldnames, dialect='market')
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')