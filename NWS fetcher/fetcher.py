import requests
import json

# Access NWS observations for Portland International Jetport and load into variable 'data'
response = requests.get("https://api.weather.gov/stations/KPWM/observations/current")
data = response.json()

# Temporary solution to access local JSON file, copied direct from above API
#filename = 'H:/GitHub/High-Power-Scoreboard/sample.json'
#if filename:
#    with open(filename,'r') as f:
#        data = json.load(f)

timestamp = data.get('properties').get('timestamp')
temperatureRaw = data.get('properties').get('temperature').get('value')
dewpointRaw = data.get('properties').get('dewpoint').get('value')
windDirectionRaw = data.get('properties').get('windDirection').get('value')
windSpeedRaw = data.get('properties').get('windSpeed').get('value')
windGustRaw = data.get('properties').get('windGust').get('value')
barometricPressureRaw = data.get('properties').get('barometricPressure').get('value')

#print(type(timestamp),type(temperatureRaw),type(dewpointRaw),type(windDirectionRaw),type(windSpeedRaw),type(windGustRaw),type(barometricPressureRaw))
#print(timestamp,temperatureRaw,dewpointRaw,windDirectionRaw,windSpeedRaw,windGustRaw,barometricPressureRaw)

# If data is empty, use 0
if temperatureRaw is None:
    temperatureRaw = 0

if dewpointRaw is None:
    dewpointRaw = 0

if windDirectionRaw is None:
    windDirectionRaw = 0

if windSpeedRaw is None:
    windSpeedRaw = 0

if windGustRaw is None:
    windGustRaw = 0

if barometricPressureRaw is None:
    barometricPressureRaw = 0

# Convert all data to integers

temperature = int(round(temperatureRaw)) # °C
dewpoint = int(round(dewpointRaw)) # °C
windDirection = int(round(windDirectionRaw)) # bearing
windSpeed = int(round(windSpeedRaw)) # m/s
windGust = int(round(windGustRaw)) # m/s
barometricPressure = int(round(barometricPressureRaw)) # Pa

# Unit conversion
temperatureF = (temperature * 9/5) + 32
dewpointF = (dewpoint * 9/5) + 32
windSpeedMPH = windSpeed * 2.2369
windGustMPH = windGust * 2.2369
windSpeedKPH = windSpeed * (3.6/1)
windGustKPH = windGust * (3.6/1)
barometricPressureHg = 0.0002952998751 * barometricPressure # Pa to inHg
barometricPressure = barometricPressure / 100

#rounding pressures
barometricPressure = round(barometricPressure,1)
barometricPressureHg = round(barometricPressureHg,2)

#calculate density altitude
#reference: https://www.weather.gov/media/epz/wxcalc/densityAltitude.pdf

#convert temperature in celsius to kelvin
airTemperature = temperature + 273.15

#calculate vapor pressure
vaporPressure = 6.11 * (10 ** ((7.5 * dewpoint)/(237.7 + dewpoint)))

#calculate virtual temperature
virtualTemperature = (airTemperature / (1 - ((vaporPressure / barometricPressure) * (0.378))))

#convert virtual temperature to Rankine
virtualTemperature = virtualTemperature * (9 / 5)

#calculate density altitude
densityAltitudeFt = 145366 * (1 - (((17.326 * barometricPressureHg) / virtualTemperature) ** 0.235))

#convert to metric
densityAltitudeM = densityAltitudeFt * 0.3048

#convert to readable format
densityAltitudeFt = int(round(densityAltitudeFt))
densityAltitudeM = int(round(densityAltitudeM))

#display results, US Customary
print('US Customary:')
print('Temperature: %d°F' % temperatureF)
print('Dewpoint: %d°F' % dewpointF)
print('Wind speed: %d MPH' % windSpeedMPH)
print('Wind gust: %d MPH' % windGustMPH)
print('Station pressure: %.2f inHg' % barometricPressureHg)
print("Density altitude: %d ft" % densityAltitudeFt)
print('\n')

#display results, Metric
print('Metric:')
print('Temperature: %d°C' % temperature)
print('Dewpoint: %d°C' % dewpoint)
print('Wind speed: %d KPH' % windSpeedKPH)
print('Wind gust: %d KPH' % windGustKPH)
print('Station pressure: %.1f hPa' % barometricPressure)
print("Density altitude: %d m" % densityAltitudeM)