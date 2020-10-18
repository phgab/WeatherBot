from weatherReader import returnWeatherInfo
from weatherMinutely import minutely
import weatherHourly

def returnMinutely(requestData):
    weatherData, coord, errorCode = returnWeatherInfo(requestData)
    if 0 <= errorCode:
        plotTitle = coord["loc"] + ", " + coord["time"]
        fileName, returnStr = minutely(weatherData["minutely"],plotTitle)
        return returnStr, fileName, errorCode
    else:
        return "", "", errorCode

# TODO: create new bot and pull the old testbot files from repo
