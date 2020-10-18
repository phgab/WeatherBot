from weatherReader import returnWeatherInfo
from weatherMinutely import minutely
import weatherHourly

def returnMinutely(requestData):
    weatherData, loc, errorCode = returnWeatherInfo(requestData)
    if 0 <= errorCode:
        fileName, returnStr = minutely(weatherData["minutely"],loc)
        return returnStr, fileName, errorCode
    else:
        return "", "", errorCode

# TODO: create new bot and pull the old testbot files from repo
