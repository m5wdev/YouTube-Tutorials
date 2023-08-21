from flask import Flask, render_template, request, redirect
import requests


app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def homepage():
#     if request.method == 'GET':
#         print('GET query')
#         # print(request.args) # GET attributes
#         print(request.args.get('username'), request.args.get('password'))

#     if request.method == 'POST':
#         print('POST query')
#         print(request.form) # POST data
#         print(request.form['username'], request.form['password'])
#     return render_template('base.html')


# https://api.weatherapi.com/v1/current.json?key=e830a0b1c1ec40e8af2114854221603&q=москва&aqi=no&lang=ru

BASE_WEATHER_API = 'https://api.weatherapi.com/v1/current.json?'
API_KEY = 'e830a0b1c1ec40e8af2114854221603'


@app.route('/')
def homepage():
    weather_data = {}
    has_data = False

    if request.method == 'GET':
        if request.args.get('reset') == '':
            return redirect('/')

        q = request.args.get('q')
        if q:
            weatherAPI_str = f'{BASE_WEATHER_API}key={API_KEY}&q={q}&aqi=no&lang=ru'
            # print(weatherAPI_str)
            weatherAPI_response = requests.get(weatherAPI_str).json()
            print(weatherAPI_response)
            weather_data = weatherAPI_response
            has_data = True

    return render_template('base.html', weather_data=weather_data, has_data=has_data)
