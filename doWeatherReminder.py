import telepot
import os
from weatherFuncts import returnMinutely, returnHourly

TOKEN = os.environ["TELTOKEN"]


def main():
    bot = telepot.Bot(TOKEN)

    [rainStr, bikeStr], fileNameMin, errorCode1 = returnMinutely({"address": "Kriegerstrasse 22, Hannover"})
    _, fileNameHrl, errorCode2 = returnHourly({"address": "Kriegerstrasse 22, Hannover"})
    returnStr = rainStr + "\n" + bikeStr

    bot.send_photo(532298931, open(fileNameHrl + ".jpg", 'rb'))
    bot.send_photo(532298931, open(fileNameMin + ".jpg", 'rb'))
    bot.sendMessage(532298931,returnStr)


if __name__ == '__main__':
    main()
