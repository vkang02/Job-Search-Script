#!/usr/bin/python

import sys
import os
import csv
import string
import webbrowser

new = 2

print sys.argv[1]

if len( sys.argv ) < 2 :
    sys.stderr.write( sys.argv[ 0 ]  + 
                      ": usage - "   + 
                      sys.argv[ 0 ]  + " [.csv file name]\n" )
    sys.exit()

if not os.path.exists(sys.argv[ 1 ]):
    sys.stderr.write( sys.argv[ 1 ] + " not found \n" )
    sys.exit()


with open( sys.argv[ 1 ], 'rb') as csvfile:
	f = open(sys.argv[1] + ".html", "w")
	table_string = "<table>"
	reader       = csv.reader( csvfile )
	print"out"
	for row in reader:
		print "in"
		table_string += "<tr>" + \
						"<td>" + \
						string.join( row, "</td><td>" ) + \
						"</td>" + \
						"</tr>\n"
	table_string += "</table>"

	#sys.stdout.write( table_string )
	f.write(table_string) 

	url = "file:///Users/vkang/Desktop/JobSearchScript/" + sys.argv[1] + ".html"
	webbrowser.open(url,new=new)
