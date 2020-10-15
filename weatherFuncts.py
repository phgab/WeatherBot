from weatherReader import findLatLon, checkNewData
import weatherMinutely
import weatherHourly

def returnWeatherInfo(requestData):
    if "coord" in requestData:
        coord = requestData["coord"]
    elif "address" in requestData:
        # TODO: Add error handling in findLatLon
        coord = findLatLon(requestData["address"])
    else:
        print("No location given")
        return [0,-1]
    returnVal = checkNewData(coord)
    return returnVal

# TODO: create new bot and pull the old testbot files from repo






