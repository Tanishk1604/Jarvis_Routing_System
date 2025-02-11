from flask import Flask, render_template, request
import requests
import time
import re  # Import regex for parsing duration strings
from datetime import datetime, timedelta, timezone

# Replace these with your actual API keys
TOMTOM_API_KEY = 'TINxeb8UBcGhcPuiYu4WuAAmSb2KBlFb'
GOOGLE_MAPS_API_KEY = 'AIzaSyC1JrSgRtVYT86yfKAarBRaFLJ1itUU-X8'
AQICN_API_KEY = '0b332e1a503a76636718ac342174088beefc1761'
OPENWEATHER_API_KEY = '1a57b21448ce17abe95b6c916cf17a8c'

app = Flask(__name__)

@app.route('/map')
def show_map():
    return render_template('map.html', APIKEY=TOMTOM_API_KEY)




def get_route(origin, destination):
    # Set departure_time to now
    departure_time = int(time.time())  # Current time in seconds since epoch
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&alternatives=true&departure_time={departure_time}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    return response.json()

def get_air_quality(location):
    try:
        url = f"https://api.waqi.info/feed/{location}/?token={AQICN_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"data": {"aqi": "N/A", "city": {"name": "Unknown"}}}
    except Exception as e:
        print(f"Error fetching air quality data: {e}")
        return {"data": {"aqi": "N/A", "city": {"name": "Unknown"}}}

def calculate_emissions(distance_km, mileage_km_per_l, emission_factor):
    fuel_consumed = distance_km / mileage_km_per_l
    co2_emissions_kg = fuel_consumed * emission_factor
    co2_emissions_g = co2_emissions_kg * 1000
    return round(co2_emissions_g, 3)  # Round to three decimal places

def calculate_toll_cost(route):
    number_of_tolls = len([step for step in route['legs'][0]['steps'] if "toll" in step['html_instructions'].lower()])
    toll_charge_per_toll = 250
    total_toll_cost = number_of_tolls * toll_charge_per_toll
    return number_of_tolls, total_toll_cost

def parse_duration(duration_str):
    """Convert a duration string like '15 hours 59 mins' to total seconds."""
    hours = 0
    minutes = 0

    # Use regex to find hours and minutes in the string
    hours_match = re.search(r'(\d+)\s*hours?', duration_str)
    if hours_match:
        hours = int(hours_match.group(1))

    minutes_match = re.search(r'(\d+)\s*mins?', duration_str)
    if minutes_match:
        minutes = int(minutes_match.group(1))

    return hours * 3600 + minutes * 60  # Convert to total seconds



def get_weather(city_name):
    """Fetch weather data from OpenWeatherMap API for a given city."""
    try:
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}'
        response = requests.get(weather_url)
        weather_info = response.json()

        if weather_info['cod'] == 200:
            kelvin = 273
            temp = int(weather_info['main']['temp'] - kelvin)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            cloudy = weather_info['clouds']['all']
            description = weather_info['weather'][0]['description']
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']
            timezone_offset = weather_info['timezone']
            sunrise_time = datetime.fromtimestamp(sunrise + timezone_offset, timezone.utc).strftime('%H:%M:%S')
            sunset_time = datetime.fromtimestamp(sunset + timezone_offset, timezone.utc).strftime('%H:%M:%S')

            return {
                "temperature": temp,
                "pressure": pressure,
                "humidity": humidity,
                "cloudy": cloudy,
                "description": description,
                "sunrise": sunrise_time,
                "sunset": sunset_time,
            }
        else:
            return {"error": f"Weather data not found for {city_name}"}
    except Exception as e:
        return {"error": f"Error fetching weather data: {e}"}



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit', methods=['POST'])
def submit():
    origin = request.form['origin']
    destination = request.form['destination']
    fuel_efficiency = float(request.form['fuel_efficiency'])
    vehicle_type = request.form['vehicle_type']

    emission_factors = {
        "Delivery Vans": 2.31,
        "Box Trucks": 2.68,
        "Tractor-Trailers": 2.68,
        "Less-Than-Truckload (LTL) Trucks": 2.68
    }

    route_data = get_route(origin, destination)
    weather_origin = get_weather(origin)
    weather_destination = get_weather(destination)

    if route_data.get('status') == 'OK':
        routes = route_data['routes']
        route_info = []

        for index, route in enumerate(routes[:3]):
            distance = route['legs'][0]['distance']['value'] / 1000
            emission_factor = emission_factors.get(vehicle_type, 0)
            emissions = calculate_emissions(distance, fuel_efficiency, emission_factor)
            
            duration_in_traffic_str = route['legs'][0].get('duration_in_traffic', {}).get('text', 'N/A')
            duration_in_traffic = parse_duration(duration_in_traffic_str)  # Parse the duration string
            
            number_of_tolls, total_toll_cost = calculate_toll_cost(route)

            # Calculate ETA
            current_time = datetime.now()
            eta = current_time + timedelta(seconds=duration_in_traffic)

            # Calculate fuel savings
            if vehicle_type == "Diesel":
                new_mileage = 12  # Example mileage for fuel-efficient route
            else:
                new_mileage = 10  # Example mileage for petrol

          
            route_info.append({
                'index': index,
                'distance': distance,
                'emissions': emissions,
                'steps': route['legs'][0]['steps'],
                'duration': route['legs'][0]['duration']['text'],
                'duration_in_traffic': duration_in_traffic_str,  # Keep this as a string for display
                'eta': eta.strftime("%Y-%m-%d %H:%M:%S"),  # Format ETA as a string
                'number_of_tolls': number_of_tolls,
                'total_toll_cost': total_toll_cost,
                
            })

        route_info.sort(key=lambda x: x['distance'])

        air_quality_data_origin = get_air_quality(origin)
        aqi_origin = air_quality_data_origin.get('data', {}).get('aqi', 'N/A')
        city_name_origin = air_quality_data_origin.get('data', {}).get('city', {}).get('name', 'Unknown City')

        air_quality_data_destination = get_air_quality(destination)
        aqi_destination = air_quality_data_destination.get('data', {}).get('aqi', 'N/A')
        city_name_destination = air_quality_data_destination.get('data', {}).get('city', {}).get('name', 'Unknown City')

        return render_template('result.html', 
                               origin=origin, 
                               destination=destination, 
                               vehicle_type=vehicle_type,
                               routes=route_info,
                               aqi_origin=aqi_origin,
                               city_name_origin=city_name_origin,
                               aqi_destination=aqi_destination,
                               city_name_destination=city_name_destination,
                               weather_origin=weather_origin,
                               weather_destination=weather_destination)
    else:
        error_message = route_data.get('error_message', 'Could not find a route.')
        return render_template('result.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)