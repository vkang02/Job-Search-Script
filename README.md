# Job-Search-Script

How the myJobSearch script works:

The script starts off by asking the user questions to specify the job search. It stores each input
into its own variable. If the user inputs a list of words, those words are then put into a list which
is split by commas. Then a REQUEST is made to Indeed's API using my publisher id: 8145859988824678. The
information is stored as a JSON object. 

The script then opens a file and names it whatever query that user has inputted plus .csv. We give the
file the append option and and call it csvFile for withiin the script. Then the labels for each column 
in the csv file is written. 

From there, we loop through the locations the user has inputted so that we can print the same number of results
for each location. We write the results in steps of 10, up to whatever max is specified. We make sure that whatever
query and location was inputted does not have any spaces and instead have '+' because this is how the
indeed url formats it. We create a final url with the query, location, radius given by user, and a number. The number
is just for keeping track of which result it is. We open the final url and then parse the json objects to a Python object.
We loop through the data from the json object and make sure none of the words specified by the user is found in the job
title before adding it to a csv file containing the results. 

An html file is created called the query plus .html. A table is written into the html file and the data from the csv file
is stored into a table. The job title column is also a link to the job post from Indeed. 
