from weatherReader import returnWeatherInfo
from weatherMinutely import minutely
import weatherHourly

def returnMinutely(requestData):
    weatherData, errorCode = returnWeatherInfo(requestData)
    if 0 <= errorCode:
        fileName, returnStr = minutely(weatherData["minutely"])
        return returnStr, fileName, errorCode
    else:
        return "", "", errorCode

# TODO: create new bot and pull the old testbot files from repo
