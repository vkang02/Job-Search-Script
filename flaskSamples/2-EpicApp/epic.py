from flask import Flask, flash, redirect, render_template, request, session, abort
 
app = Flask(__name__)
 
@app.route("/")
def index():
    return "Flask App! Visit <a href='http://127.0.0.1:81/hello/Jackson/'>http://127.0.0.1/hello/Jackson/</a> "
 
@app.route("/hello/<string:name>/")
def hello(name):
    return render_template(
        'test.html',name=name)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
