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
glassdoorUrl = 'http://api.glassdoor.com/api/api.htm?t.p=118132&t.k=f7epqLmorMI&userip=0.0.0.0&useragent=&format=json&v=1&action=employers'
#glassdoorUrl = 'http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=118132&t.k=f7epqLmorMI&action=jobs&q=web+developer&userip=10.0.0.7&useragent=Chrome/55.0.2883.95'

query = raw_input("What kind of job are you looking for? i.e. 'Software Engineer' ")
location = raw_input("Where do you want to work? i.e. 'San Francisco, Seattle, ...' ")
radius = raw_input("How far (in miles) from the location are you willing to go? i.e. '50' ")
excludeWords = raw_input("List any words that should not be in the job title and separate them with commas(case-sensitive): ")
companyType = raw_input("Do you want to only show public companies? (True/False) ")
#maxRes = raw_input("How many results would you like to see for each location? ")


#countries = set(['us','ar','au','at','bh','be','br','ca','cl','cn','co','cz','dk','fi','fr','de','gr','hk','hu','in','id','ie','il','it','jp','kr','kw','lu','my','mx','nl','nz','no','om','pk','pe','ph','pl','pt','qa','ro','ru','sa','sg','za','es','se','ch','tw','tr','ae','gb','ve'])
num = 0
new = 2
pn = 1
notFound = True
myLocs = location.split(",")
exclude = excludeWords.split(",")
#exclude = ("senior", "Senior", "sr", "Sr", "Sr.", "sr.")

# #Creates 
# grabforNum = requests.get(indeedUrl)
# json_content = json.loads(grabforNum.content)
# print(json_content["totalResults"])
# totalres = (json_content["totalResults"])


def column(matrix, i):
    return [row[i] for row in matrix]

def search(values, searchFor):
    for k in values:
        for v in values[k]:
            if searchFor in v:
                return k
    return None

with open(query + ".csv", "a") as csvFile:
		with open('constituents.csv', 'rb') as f:
			reader = csv.reader(f)
			theList = list(reader)

			results = csv.writer(csvFile)
			
			for l in myLocs:
				for num in range(0, 5, 2):
					term = query.replace(' ', '+')
					loc = l.replace(' ', '+')

					final_indeed_url = indeedUrl + '&q=' + term + '&radius=' + radius + '&l=' + loc + '&start=' + str(num)
					json_obj = urllib2.urlopen(final_indeed_url)
					data = json.load(json_obj)
					print 'Complete '+ final_indeed_url

					for item in data['results']:
						while(notFound and pn<5):
							final_glassdoor_url = glassdoorUrl + '&q=' + '&l=' + loc + '&pn=' + str(pn)
							req = urllib2.Request(final_glassdoor_url, headers={'User-Agent': 'Magic Browser'})
							con = urllib2.urlopen(req)
							data2 = json.load(con)
							for entry in data2['response']['employers']:
								if(entry['name'] == item['company']):
									#If any of the excluded words are in the job title, continue and don't add the job title to the results
									if any(lvl in item['jobtitle'].encode('utf-8') for lvl in exclude):	
										continue
									#If the user wants to see only public companies from the S&P 500 List, display only those results
									elif(companyType == "True" or companyType == "true" or companyType =="t" or companyType =="T"):
										if(item['company'].encode('utf-8') in column(theList, 1)):
											results.writerow([item['formattedRelativeTime'].encode('utf-8'), item['jobtitle'].encode('utf-8'), item['company'].encode('utf-8'), item['formattedLocation'].encode('utf-8'), item['url'].encode('utf-8'), entry['overallRating'].encode('utf-8')])
											notFound = False
											print "in"
									#Display everything 
									else:
										results.writerow([item['formattedRelativeTime'].encode('utf-8'), item['jobtitle'].encode('utf-8'), item['company'].encode('utf-8'), item['formattedLocation'].encode('utf-8'), item['url'].encode('utf-8'), entry['overallRating'].encode('utf-8')])
										notFound = False
										print "in"
							pn = pn+1
							print "out"
						notFound = True
						pn = 1
						print "more out"
		csvFile.close();

with open(query + ".csv", "rb") as csvFile:
	
	f = open(query + ".html", "w")
	table_string = "<html><head><title>WhatNow</title><link rel='stylesheet' type='text/css' href='myJobSearch.css'><link href='https://fonts.googleapis.com/css?family=Arvo' rel='stylesheet'><link rel='stylesheet' type='text/css' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'></head><body>"
	table_string += "<table class='table table-bordered'><tr><th>Post Age</th><th>Job Title</th><th>Company</th><th>Location</th><th>Glassdoor Rating</th></tr>"
	reader = csv.reader( csvFile )
	#Create a table in the html file. Make the Job title a link to the actual job post
	for row in reader:
		table_string += "<tr>" + \
						"<td>" +\
						row[0] + \
						"</td><td>" + \
						"<a href='" + \
						row[4]+ \
						"'>" + \
						row[1] + \
						"</a>" + \
						"</td><td>" + \
						row[2] +\
						"</td><td>" + \
						row[3] + \
						"</td><td>" + \
						row[5] + \
						"</td><td></td>" + \
						"</tr>\n"
	table_string += "</table></body>"
	    
	f.write(table_string)
	# open an HTML file on my computer
	url = "file:///Users/vkang/Desktop/JobSearchScript/" + query + ".html"
	webbrowser.open(url,new=new)

	f.close()


