from flask_app import app
from flask import render_template , redirect
from flask import jsonify
from flask_app.models.weather import Weather
import requests
from requests.exceptions import RequestException
import threading
import time


API_URL = "https://melchior.moja.it:8085/weather-api/get_weather?lat=41.3281007&lon=139.6917"


@app.route('/', methods=['GET'])
def get_weather():
    
        try:
            # Make GET request to the API
            response = requests.get(API_URL)
            
            # Check if the request was successful
            if response.status_code == 200:
                
                weather_data = response.json()  # Convert response to JSON format

                # Extract relevant data from weather_data
                current_temp = weather_data.get('current_temp')
                feels_like = weather_data.get('feels_like')
                weather_description = weather_data.get('weather_description')

                # Save to database
                save_to_database({
                    'current_temp': current_temp,
                    'feels_like': feels_like,
                    'weather_description': weather_description
                    
                })
                # Background thread to run fetch_weather_data every 5 minutes
                def background_thread():
                    
                        get_weather()
                        time.sleep(300)
                        
                        
                
                # Start the background thread
                thread = threading.Thread(target=background_thread)
                thread.start()
                
                weather_history = Weather.get_weather_data()
                
                return render_template('index.html', current_temp=current_temp, feels_like=feels_like, weather_description=weather_description,weather_conditions=weather_conditions,weather_icons=weather_icons,weather_history=weather_history)
                

            else:
                weather_data = Weather.get_weather_data()
                return ("Couldn't fetch data")

        except RequestException as e:
            return jsonify({'error': str(e)}), 500
        


def save_to_database(weather_data):
    # Insert data into the database using Weather model
    Weather.insert_data(weather_data)
    
#Creating the lists that will be used in the pics logic
weather_conditions = ["clear sky","few clouds","broken clouds","shower rain","rain","thunderstorm","snow","mist","overcast clouds","moderate rain","scattered clouds"]
weather_icons=["../static/icons/clear_sky.png","../static/icons/few_clouds.png","../static/icons/scattered_clouds.png","../static/icons/shower_rain.png","../static/icons/rain.png","../static/icons/thunderstorm.png","../static/icons/snow.png","../static/icons/mist.png","../static/icons/scattered_clouds.png","../static/icons/shower_rain.png","../static/icons/scattered_clouds.png"]

