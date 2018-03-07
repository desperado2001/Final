from flask import Flask, render_template, redirect, request, url_for, make_response
import redis
import os
import json
import matplotlib.pyplot as plt
import mpld3
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpld3._server import serve


if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
    r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
else:
    r = redis.Redis(host='127.0.0.1', port='14936')

app = Flask(__name__)

accel = r.lrange('accelerometer',0,-1)
dist = r.lrange('distance',0,-1)
gyro = r.lrange('gyroscope',0,-1)
humid = r.lrange('humidity',0,-1)
light = r.lrange('light',0,-1)
temperature = r.lrange('temperature',0,-1)

ddist = dist[-1]
dgyro = gyro[-1]
dhumid = humid[-1]
dlight = light[-1]
dtemp = temperature[-1]
daccel = accel[-1]


#plt.figure(1)
#plt.subplot(411)
#plt.plot(dist)

#plt.subplot(412)
#plt.plot(light)

#plt.subplot(413)
#plt.plot(temperature)

#plt.subplot(414)
#plt.plot(humid)
#plt.show()


@app.route('/')
def home():
        return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')
	
	
@app.route('/content/')
def content():
	return render_template('content.html', daccel = daccel, 
	ddist = ddist, dgyro = dgyro, dhumid = dhumid, dlight = dlight, dtemp = dtemp
	)

@app.route('/temp/')
def temp():
	return render_template('temp.html', temperature =range(10))


@app.route('/graph/')
def graph():
	fig1 = plt.figure()
	plt.title("temperature")
	plt.plot(temperature)
	html1 = mpld3.fig_to_html(fig1)

	fig2 =plt.figure()
	plt.title("distance")
	plt.plot(dist)

	# create html for both graphs 
	html1 = mpld3.fig_to_html(fig1)
	html2 = mpld3.fig_to_html(fig2)
	# serve joined html to browser
	return (html1 + html2)

	
if __name__ == "__main__":
                app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '5000')), threaded=True)

				
