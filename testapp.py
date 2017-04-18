from flask import Flask, render_template, flash, request, url_for, redirect, session
import urllib2
import json
import csv
import requests
import sys
import os
import string
 

reload(sys)  
sys.setdefaultencoding('utf8')

app = Flask('testapp')

@app.route('/', methods=["GET","POST"])
def index():
	if request.method == "POST":
		session['query'] = request.form['job']
		location = request.form['location']
		excludeWords = request.form['exclude']
		radius = request.form['radius']
		companyType = request.form['companyType']

		indeedUrl = 'http://api.indeed.com/ads/apisearch?publisher=8145859988824678&v=2&limit=100&format=json'
		glassdoorUrl = 'http://api.glassdoor.com/api/api.htm?t.p=118132&t.k=f7epqLmorMI&userip=0.0.0.0&useragent=&format=json&v=1&action=employers'

		num = 0
		new = 2
		myLocs = location.split(",")
		exclude = excludeWords.split(",")
		with open(session['query'] + ".csv", "a") as csvFile:
				with open('constituents.csv', 'rb') as f:
					reader = csv.reader(f)
					theList = list(reader)

					results = csv.writer(csvFile)
					#results.writerow(["Date Posted", "Position Title", "Company Name", "Location", "Link"])
					
					for l in myLocs:
						for num in range(0, 100, 10):
							term = session['query'].replace(' ', '+')
							loc = l.replace(' ', '+')
						
							final_url = indeedUrl + '&q=' + term + '&radius=' + radius + '&l=' + loc + '&start=' + str(num)
							json_obj = urllib2.urlopen(final_url)
							data = json.load(json_obj)
							print 'Complete '+ final_url

							for item in data['results']:
								#If any of the excluded words are in the job title, continue and don't add the job title to the results
								if any(lvl in item['jobtitle'].encode('utf-8') for lvl in exclude):	
									continue
								#If the user wants to see only public companies from the S&P 500 List, display only those results
								elif(companyType == "True" or companyType == "true" or companyType =="t" or companyType =="T"):
									if(item['company'].encode('utf-8') in (row[1] for row in theList)):
										results.writerow([item['jobkey'].encode('utf-8'), item['formattedRelativeTime'].encode('utf-8'), item['jobtitle'].encode('utf-8'), item['company'].encode('utf-8'), item['formattedLocation'].encode('utf-8'), item['url'].encode('utf-8')])
								#Display everything 
								else:
									results.writerow([item['jobkey'].encode('utf-8'),item['formattedRelativeTime'].encode('utf-8'), item['jobtitle'].encode('utf-8'), item['company'].encode('utf-8'), item['formattedLocation'].encode('utf-8'), item['url'].encode('utf-8')])
				csvFile.close();
		
		return redirect(url_for('results'))
	return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html') 


@app.route('/results')
def results():
	query = session.get('query', None)
	reader = csv.reader(open(query + '.csv'))

	return render_template('results.html', result = reader)

if __name__ == '__main__':
	app.secret_key = os.urandom(24)
	app.run()