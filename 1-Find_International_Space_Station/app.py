from flask import Flask ,request, jsonify, Markup, render_template
import base64
import io
import os
import matplotlib.pyplot as plt
import requests
import sys
import matplotlib
from haversine import haversine
import datetime

app = Flask(__name__)

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

def current_iss_location():
    
    request = requests.get(url='http://api.open-notify.org/iss-now.json')
    iss_location = request.json()
    
    iss_lon = float(iss_location['iss_position']['longitude'])
    iss_lat = float(iss_location['iss_position']['latitude'])
    
    return (iss_lat, iss_lon)

def current_iss_astros():
        
    request = requests.get(url='http://api.open-notify.org/astros.json')
    iss_astros = request.json()
    
    astronauts_iss = [n['name'] for n in iss_astros['people']]
    num_of_astros = iss_astros['number']
    
    return astronauts_iss, num_of_astros

def get_user_info():
    
    request = requests.get('http://ipinfo.io/json')
    user_info = request.json()
    
    user_city = user_info['city']
    user_lat, user_lon = [float(i) for i in user_info['loc'].split(',')]
    user_country = user_info['country']
   
    return user_lat, user_lon, user_city

def get_expected_time_above_me(user_lat, user_lon):
    
    EXPECTED_URL = "http://api.open-notify.org/iss-pass.json?lat="+str(user_lat)+"&lon="+str(user_lon)+"&n=3"
    
    request = requests.get(EXPECTED_URL)
    
    expected_info = request.json()
    next_fly_by = expected_info['response'][0]['risetime']
    second_fly_by = expected_info['response'][1]['risetime']
    
    this_flyby_utc_timestamp = datetime.datetime.fromtimestamp(next_fly_by).strftime('%d %b at %H:%M:%S')
    next_flyby_utc_timestamp = datetime.datetime.fromtimestamp(second_fly_by).strftime('%d %b at %H:%M:%S')
    
    return this_flyby_utc_timestamp, next_flyby_utc_timestamp
    
def distance_between_user_and_iss(*,user_lat,user_lon,iss_lat,iss_lon):
    
    user_tuple = (user_lat,user_lon)
    iss_tuple = (iss_lat, iss_lon)
    
    return round(haversine(user_tuple, iss_tuple),2)
    
@app.route("/",methods=['GET','POST'])
def ISS_tracker():
    
    google_map_url = "https://maps.google.com/maps?z=1&output=embed&t=h"
    
    user_lat, user_lon, user_city = get_user_info()
    
    expected_flyby_time, next_flyby_time = get_expected_time_above_me(user_lat, user_lon)
    
    astros_list, num_of_astros = current_iss_astros()
    
    your_distance_from_iss = None
        
    if request.method == 'POST':
        
        iss_lat, iss_lon = current_iss_location()
        
        your_distance_from_iss = distance_between_user_and_iss(user_lat= user_lat,user_lon= user_lon,iss_lat=iss_lat,iss_lon=iss_lon)

        google_map_url = "https://maps.google.com/maps?q={},{}&z=2&output=embed&t=k".format(str(iss_lat),str(iss_lon))
    
    return render_template('iss.html',google_map = google_map_url, your_distance_from_iss=your_distance_from_iss,
                           expected_flyby_time= expected_flyby_time,user_city=user_city,
                           user_lat=user_lat, user_lon=user_lon,
                           astros_list=astros_list,num_of_astros=num_of_astros,next_flyby_time=next_flyby_time)
    
if __name__ == '__main__':
    app.run(debug=True)