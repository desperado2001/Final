from flask import Flask, render_template, redirect, request, url_for, make_response
import redis
import os
import json

r = redis.Redis(host='127.0.0.1', port='6379', password='vagrant')

app = Flask(__name__)


def data():
    temp = r.lrange('temperature',0,-1)
    movement =  r.lrange('movement',0,-1)
    distance =  r.lrange('distance',0,-1)
    light = r.lrange('light',0,-1)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')
	
	
@app.route('/content/')
def content():
	return render_template('content.html')


	
if __name__ == '__main__':
    app.run(debug=True)