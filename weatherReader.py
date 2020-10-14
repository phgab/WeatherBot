import pickle
import os.path
import time
import requests
import urllib.parse



def findLatLon(address):
    url = 'https://nominatim.openstreetmap.org/search/' + \
          urllib.parse.quote(address) + '?format=json'

    response = requests.get(url).json()
    lat = response[0]["lat"]
    lon = response[0]["lon"]
    coord = {
        "lat": lat,
        "lon": lon
    }
    return coord



def checkNewData(coord):
    # If there has been new data within the last n minutes don't renew, else get and save
    returnVal = 0
    if os.path.isfile("weatherData"):
        returnVal = 1
        data = pickle.load(open("weatherData", "rb"))
        tNow = int(time.time())
        tLast = data["tLast"]
        if 60*5 < (tNow - tLast):  # only get new data every 5 mins
            returnVal = 2
            print("10 minutes have passed, new data is acquired")
            data = getNewData(coord)
            pickle.dump(data, open("weatherData", "wb"))
        if False:
            if coord[0] != data["lat"] or coord[1] != data["lon"]:
                returnVal = 3
                print("Geodata has changed, new data is acquired")
                data = getNewData(coord)
                pickle.dump(data, open("weatherData", "wb"))

    else:
        data = getNewData(coord)
        pickle.dump(data, open("weatherData", "wb"))
    return [data, returnVal]



def getNewData(coord):
    api_key = os.environ["OWMAPI"]  # added through heroku config:add TOKEN=…
    # oneCall API
    base_url = "https://api.openweathermap.org/data/2.5/onecall?lat="
    lat = coord["lat"]
    lon = coord["lon"]
    complete_url = base_url + str(lat) + "&lon=" + str(lon) + \
                   "&units=metric&lang=de" + \
                   "&appid=" + api_key

    response = requests.get(complete_url)
    data = response.json()

    tNow = int(time.time())
    data["tLast"] = tNow
    return data
