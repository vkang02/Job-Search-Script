from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json
import urllib2
 
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
 
def getExchangeRates():
    rates = []
    response = urllib2.urlopen('http://api.fixer.io/latest')
    data = response.read()
    rdata = json.loads(data, parse_float=float)
 
    rates.append( rdata['rates']['USD'] )
    rates.append( rdata['rates']['GBP'] )
    rates.append( rdata['rates']['HKD'] )
    rates.append( rdata['rates']['AUD'] )
    return rates
 
@app.route("/")
def index():
    rates = getExchangeRates()
    return render_template('test.html',**locals())      
 
@app.route("/hello")
def hello():
    return "Hello World!"
 
 
if __name__ == "__main__":
    app.run()
