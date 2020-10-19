from weatherReader import returnWeatherInfo
from weatherMinutely import minutely
from weatherHourly import hourly

def returnMinutely(requestData):
    weatherData, coord, errorCode = returnWeatherInfo(requestData)
    if 0 <= errorCode:
        plotTitle = coord["place"] + ", " + coord["time"]
        fileName, returnStr = minutely(weatherData["minutely"],plotTitle)
        fileName2, returnStr2 = hourly(weatherData["hourly"], plotTitle)
        return returnStr, fileName, errorCode
    else:
        return "", "", errorCode

def returnHourly(requestData):
    weatherData, coord, errorCode = returnWeatherInfo(requestData)
    if 0 <= errorCode:
        plotTitle = coord["place"] + ", " + coord["time"]
        fileName, returnStr = hourly(weatherData["hourly"], plotTitle)
        return returnStr, fileName, errorCode
    else:
        return "", "", errorCode

