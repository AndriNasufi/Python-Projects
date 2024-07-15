from flask_app import app
from flask import render_template, request, redirect
from flask import jsonify
import json
from flask_app.models.weather import Weather


@app.route('/')
def homepage():
    return render_template('index.html')

API_URL = "https://melchior.moja.it:8085/weather-api/get_weather"

# Route to fetch weather data
@app.route('/weather', methods=['GET'])

def get_weather():
    # Example latitude and longitude
    lat = 41.3281007
    lon = 139.6917
    # Parameters for the API request
    params = {
        'lat': lat,
        'lon': lon
    }

    try:
        # Make GET request to the API
        response = request.get(API_URL, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            weather_data = response.json()  # Convert response to JSON format
            print(20)
            return jsonify(weather_data)   # Return weather data as JSON response
            
        else:
            print(21)
            return jsonify({'error': 'Failed to fetch weather data'}), response.status_code

    except request.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    

def save_to_database(weather_data):
    # Extract relevant data from weather_data
    data = {
        'current_temp': weather_data.get('temperature', {}).get('current'),
        'feels_like': weather_data.get('temperature', {}).get('feels_like'),
        'weather_description': weather_data.get('weather', {}).get('description')
    }

    # Insert data into the database using Weather model
    Weather.insert_data(data)