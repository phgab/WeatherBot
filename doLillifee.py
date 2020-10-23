import telepot
import os
from getRandomImage import get_img
#from weatherFuncts import findLatLon, checkNewData, getMinutely, evalMinutely, plotMinutelyPrec

TOKEN = os.environ["TELTOKEN"]


def main():
    bot = telepot.Bot(TOKEN)

    imgUrl = get_img("Lillifee")


    # fileName = "minutelyRain"
    # address = "Kriegerstrasse 22, 30161 Hannover"
    # coord = findLatLon(address)
    # data = checkNewData(coord)
    # minutely = getMinutely(data["minutely"])
    # returnStr = evalMinutely(minutely)
    # plotMinutelyPrec(minutely, fileName)

    bot.sendPhoto(532298931, imgUrl)
    bot.sendMessage(532298931, "lillifee sent")


if __name__ == '__main__':
    main()
