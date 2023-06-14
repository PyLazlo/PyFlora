import datetime
import requests
#from geopy import Nominatim


# def get_location(location):

#     geolocator = Nominatim(user_agent="PyWeather")
#     location = geolocator.geocode(location)
    
#     lat= f"{location.latitude:.2f}"
#     long = f"{location.longitude:.2f}"
#     URL = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m,relativehumidity_2m,surface_pressure'
#     return URL

def get_data_from_url():
    """
    Returns a string. If it can get the data from the Weather api it will return
    the temperature value of the current hour for Zagreb.

    If it fails to connect to api it will return a string "Cannot connect"

    The string is then used for print in Pot Info 
    """
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=45.81&longitude=15.98&hourly=temperature_2m")
        if response.status_code == requests.codes.ok:
            json_from_url = response.json()
        
        else:
            return 'Cannot connect.'
    
    except Exception as e:
        print(f"Error: {e}")

    # get the current time in isoformat (same format used in api) and slice the first 14 characters
    # then add "00" to the string to get value from json for the full hour
    date = datetime.datetime.now().isoformat()[0:14]
    date= date + "00"
    list_index = json_from_url["hourly"]["time"].index(date)
    current_temp = float(json_from_url["hourly"]["temperature_2m"][list_index])

    return current_temp

