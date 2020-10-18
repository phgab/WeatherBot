from weatherReader import returnWeatherInfo
from weatherMinutely import minutely
from weatherHourly import hourly

def returnMinutely(requestData):
    weatherData, coord, errorCode = returnWeatherInfo(requestData)
    if 0 <= errorCode:
        plotTitle = coord["loc"] + ", " + coord["time"]
        fileName, returnStr = minutely(weatherData["minutely"],plotTitle)
        fileName2, returnStr2 = hourly(weatherData["hourly"], plotTitle)
        return returnStr, fileName, errorCode
    else:
        return "", "", errorCode

# TODO: create new bot and pull the old testbot files from repo
