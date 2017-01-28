#!/usr/bin/env python

# HOW TO RUN THIS SCRIPT: Open the python interpretor by going to the terminal and typing "python"
# then to load the file execute the command: execfile('myJobSearch.py'). Then call answer the questions. 
# Location can be a city, a state, zip code

import urllib2
import json
import csv
import requests
import sys
import os
import string
import webbrowser

# the function to search for a job (query). It will currently print out the job title, the company name, 
# location, and url to the job description in a csv file called "query you input".csv
#def search_indeed(query, location, radius):

# the url for the Indeed Api with the following publisher id: 8145859988824678
indeedUrl = 'http://api.indeed.com/ads/apisearch?publisher=8145859988824678&v=2&limit=100&format=json'

query = raw_input("What kind of job are you looking for? i.e. 'Software Engineer' ")
location = raw_input("Where do you want to work? i.e. 'San Francisco, Seattle, ...' ")
radius = raw_input("How far (in miles) from the location are you willing to go? i.e. '50' ")
excludeWords = raw_input("List any words that should not be in the job title and separate them with commas(case-sensitive): ")
#maxRes = raw_input("How many results would you like to see for each location? ")


#glassdoorUrl = 'http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=118132&t.k=f7epqLmorMI&action=jobs&q=web+developer&userip=10.0.0.7&useragent=Chrome/55.0.2883.95'
#countries = set(['us','ar','au','at','bh','be','br','ca','cl','cn','co','cz','dk','fi','fr','de','gr','hk','hu','in','id','ie','il','it','jp','kr','kw','lu','my','mx','nl','nz','no','om','pk','pe','ph','pl','pt','qa','ro','ru','sa','sg','za','es','se','ch','tw','tr','ae','gb','ve'])
num = 0
new = 2
myLocs = location.split(",")
exclude = excludeWords.split(",")
#exclude = ("senior", "Senior", "sr", "Sr", "Sr.", "sr.")
	
grabforNum = requests.get(indeedUrl)
json_content = json.loads(grabforNum.content)
print(json_content["totalResults"])

totalres = (json_content["totalResults"])

with open(query + ".csv", "a") as csvFile:
	results = csv.writer(csvFile)
	results.writerow(['Post Age', 'Date Created', 'Job Title', 'Company', 'Location', 'URL', 'Job Key'])
	
	for l in myLocs:
		for num in range(0, 100, 10):
			term = query.replace(' ', '+')
			loc = l.replace(' ', '+')
		
			final_url = indeedUrl + '&q=' + term + '&radius=' + radius + '&l=' + loc + '&start=' + str(num)
			json_obj = urllib2.urlopen(final_url)
			data = json.load(json_obj)
			print 'Complete '+ final_url

			for item in data['results']:
				if any(lvl in item['jobtitle'].encode('utf-8') for lvl in exclude):	
					continue
				else:
					results.writerow([item['formattedRelativeTime'].encode('utf-8'), item['date'].encode('utf-8'), item['jobtitle'].encode('utf-8'), item['company'].encode('utf-8'), item['formattedLocation'].encode('utf-8'), item['url'].encode('utf-8'), item['jobkey'].encode('utf-8')])
	csvFile.close();

with open(query + ".csv", "rb") as csvFile:
	
	f = open(query + ".html", "w")
	table_string = "<table>"
	reader = csv.reader( csvFile )
	for row in reader:
		table_string += "<tr>" + \
						"<td>" + \
						string.join( row, "</td><td>" ) + \
						"</td>" + \
						"</tr>\n"
	table_string += "</table>"
	    
	f.write(table_string)
	#sys.stdout.write( table_string ) 
	# open an HTML file on my own (Windows) computer
	url = "file:///Users/vkang/Desktop/JobSearchScript/" + query + ".html"
	webbrowser.open(url,new=new)

	f.close()


