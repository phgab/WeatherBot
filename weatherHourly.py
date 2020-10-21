import matplotlib.pyplot as plt
import time
from datetime import datetime


def hourly(hrlyData, plotTitle):
    hourly = getHourly(hrlyData)
    #returnStr = evalourly(hourly)
    hour, min = map(int, time.strftime("%H %M").split())
    fileName = "hrl_" + str(hour) + "_" + str(min)
    plotHourlyPrec(hourly, fileName, plotTitle)
    return fileName, ""


def plotHourlyPrec(hourly, fileName, plotTitle):
    dt = hourly["dt"]
    temp = hourly["temp"]
    feels_like = hourly["feels_like"]
    dt_zero = [t - dt[0] for t in dt]
    hours = [t / 3600 for t in dt_zero]
    # TODO: Add real time for x axis

    dt_text = [datetime.fromtimestamp(t).strftime("%H:%M") for t in dt]

    dt_labelText = [dt_text[idx] for idx in range(0, 48, 8)]
    dt_labelText.append("")
    dt_labelTicks = [hours[idx] for idx in range(0, 48, 8)]
    dt_labelTicks.append(48)


    fig = plt.figure()

    if "prec" in hourly:
        prec = hourly["prec"]
        ax = plt.gca()
        ax2 = ax.twinx()

        ax.plot(hours, prec)
        ax.fill_between(hours, prec)
        ax.set_yticks([0.3, 2, 7], ["leicht", "mittel", "stark"])
        if max(prec) < 10:
            ax.set_ylim(0, 10)
    else:
        ax2 = plt.gca()

    ax2.plot(hours, temp)
    ax2.plot(hours, feels_like)
    ax2.legend(["Temperatur", "Gefühlt wie"])
    ax2.set_xlabel("Zeit [h]")

    plt.title("Temperatur in " + plotTitle)

    ax2.set_xticks(dt_labelTicks)
    ax2.set_xticklabels(dt_labelText)

    plt.show(block=False)
    #print(max(prec))

    plt.savefig(fileName + ".jpg")
    # Image.open(fileName + ".png").save(fileName + '.jpg', 'JPEG')
    plt.close()


def evalHourly(minutely):
    prec = minutely[1]
    mins = range(61)
    rainStr = ""
    bikeStr = ""
    searchMin = True

    if max(prec) == 0:
        rainStr += "Kein Regen in der nächsten Stunde."
        searchMin = False
    elif max(prec) < 0.5:
        rainStr += "Nur leichter Regen."
    elif 4 < min(prec):
        rainStr += "Es regnet die ganze nächste Stunde stark!"
    elif 1 < min(prec):
        rainStr += "Es regnet die ganze nächste Stunde."
        if 4 < max(prec):
            rainStr += " Zwischendurch stark."
    else:
        rainStr += "Wechselhafter Regen in der nächsten Stunde."

    if searchMin:
        commuteTime = 20
        minIgnorePrec = 0.1 * commuteTime  # Range within values are equal to min or a bit higher
        numSlots = len(mins) - commuteTime + 1
        precSlots = [None] * numSlots
        precSlots_predict = [None] * (commuteTime - 1)

        for idx in range(numSlots):
            precSlots[idx] = sum(prec[idx:idx + commuteTime])

        for idx in range(commuteTime - 1):
            # Pretend the weather will stay like the last minute
            # could use value for the next hour or so
            precSlots_predict[idx] = sum(prec[(numSlots + idx):]) + prec[-1] * (idx + 1)

        # Evaluate the results
        allSlots = precSlots + precSlots_predict
        minPrecSlot = min(allSlots)
        indices = [i for i, x in enumerate(allSlots) if x < minPrecSlot + minIgnorePrec]

        # Eliminate neighbours
        minRecommended = []
        idxStart = 0
        idxCurr = 0
        idxNext = 1
        while idxStart < (len(indices)):
            if indices[idxCurr] + 1 == indices[idxNext]:
                if idxNext < len(indices) - 1:
                    idxCurr += 1
                    idxNext += 1
                else:
                    minRecommended.append([idxStart, idxNext])
                    break
            else:
                if idxCurr == idxStart:
                    minRecommended.append([idxStart])
                else:
                    minRecommended.append([idxStart, idxCurr])
                if idxNext < len(indices) - 1:
                    idxStart = idxNext
                    idxCurr = idxStart
                    idxNext = idxCurr + 1
                else:
                    minRecommended.append([idxNext])
                    break

        print(len(minRecommended))

        if 1 < len(minRecommended):
            bikeStr += "Die besten Startzeiten sind "
        else:
            bikeStr += "Die beste Startzeit ist "

        for idx in range(len(minRecommended)):
            if 0 < idx:
                bikeStr += " oder "
            if len(minRecommended[idx]) == 1:
                bikeStr += "in " + str(indices[minRecommended[idx][0]]) + " Minuten"
            else:
                bikeStr += "in " + str(indices[minRecommended[idx][0]]) + \
                             " - " + str(indices[minRecommended[idx][1]]) + " Minuten"
    print(bikeStr)
    return rainStr, bikeStr


def getHourly(hrlData):
    # requires ["hourly"] key from base data set
    dt = [d["dt"] for d in hrlData]
    #dt = [d["dt"] + hrlData["timezone_offset"] for d in hrlData]
    temp = [d["temp"] for d in hrlData]
    feels_like = [d["feels_like"] for d in hrlData]
    if "precipitation" in hrlData:
        prec = [d["precipitation"] for d in hrlData]
        hourly = {"dt": dt,
                  "precipitation": prec,
                  "temp": temp,
                  "feels_like": feels_like}
    else:
        hourly = {"dt": dt,
                  "temp": temp,
                  "feels_like": feels_like}
    return hourly