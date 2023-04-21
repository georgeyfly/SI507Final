from flask import Flask, render_template, request
import requests
from tree import *

app = Flask(__name__)
@app.route('/')
def index():
    return '<h1>Welcome!</h1> <h2>This is SI507 Final Demo For Qiaozhi Huang!</h2>'

@app.route('/demo')
def demo():
     
    return render_template('input.html')

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    q1 = request.form["q1"]
    q2 = request.form["q2"]
    q3 = request.form["q3"]
    q4 = request.form["q4"]
    q5 = request.form["q5"]
    job_desired = main(q1, q2, q3, q4)
    if job_desired == None:
        return '<h1> No suitable job!</h1>'
    else:
        return render_template('response.html', jobs=job_desired, demo=q5)

if __name__ == '__main__':
    print('starting Flask app', app.name)  
    app.run(debug=True)