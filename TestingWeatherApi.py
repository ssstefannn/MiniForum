import requests
import sys

location = sys.argv[1]

def get_weather():
    r = requests.get(f'https://api.weatherapi.com/v1/current.json?key=da5747a6435d497e8b3145229231604&q={location}&aqi=no', 
                 headers={'Accept': 'application/json'})
    current = r.json()['current']
    temp = current['temp_c']
    precipitation = current['precip_mm']
    pressure = current['pressure_mb']
    wind = current['wind_kph']
    condition = current['condition']['text']
    print(f'Temperature: {temp}°C')
    print(f'Precipitation: {precipitation}mm')
    print(f'Pressure: {pressure}mbar')
    print(f'Wind: {wind}kph')
    print(f'Overall: {condition}')

get_weather()