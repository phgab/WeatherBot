import telepot
import os
from getRandomImage import get_img
#from weatherFuncts import findLatLon, checkNewData, getMinutely, evalMinutely, plotMinutelyPrec

TOKEN = os.environ["TELTOKEN"]


def main():
    bot = telepot.Bot(TOKEN)

    imgUrl = get_img("Lillifee")

    bot.sendPhoto(1360677999, imgUrl)
    bot.sendMessage(1360677999, "Ihre tägliche Dosis Lillifee")
    bot.sendMessage(532298931, "lillifee sent")


if __name__ == '__main__':
    main()
