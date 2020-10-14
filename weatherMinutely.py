import matplotlib.pyplot as plt



def doRainMins(coord, fileName):
    [data, returnVal] = checkNewData(coord)
    minutely = getMinutely(data["minutely"])
    returnStr = evalMinutely(minutely)
    plotMinutelyPrec(minutely, fileName)
    return returnStr


def plotMinutelyPrec(minutely, fileName):
    dt = minutely[0]
    prec = minutely[1]
    dt_zero = [t - dt[0] for t in dt]
    minutes = [t / 60 for t in dt_zero]

    fig = plt.figure()

    plt.plot(minutes, prec)
    plt.fill_between(minutes, prec)

    plt.yticks([0.3, 2, 7], ["leicht", "mittel", "stark"])
    if max(prec) < 10:
        plt.ylim(0, 10)

    plt.show(block=False)
    print(max(prec))

    plt.savefig(fileName + ".jpg")
    # Image.open(fileName + ".png").save(fileName + '.jpg', 'JPEG')
    plt.close()


def evalMinutely(minutely):
    prec = minutely[1]
    mins = range(61)
    returnStr = ""
    searchMin = True

    if max(prec) == 0:
        returnStr += "Kein Regen in der nächsten Stunde."
        searchMin = False
    elif max(prec) < 0.5:
        returnStr += "Nur leichter Regen."
    elif 4 < min(prec):
        returnStr += "Es regnet die ganze nächste Stunde stark!"
    elif 1 < min(prec):
        returnStr += "Es regnet die ganze nächste Stunde."
        if 4 < max(prec):
            returnStr += " Zwischendurch stark."
    else:
        returnStr += "Wechselhafter Regen in der nächsten Stunde."

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
        returnStr += "\n"
        if 1 < len(minRecommended):
            returnStr += "Die besten Startzeiten sind "
        else:
            returnStr += "Die beste Startzeit ist "

        for idx in range(len(minRecommended)):
            if 0 < idx:
                returnStr += " oder "
            if len(minRecommended[idx]) == 1:
                returnStr += "in " + str(indices[minRecommended[idx][0]]) + " Minuten"
            else:
                returnStr += "in " + str(indices[minRecommended[idx][0]]) + \
                             " - " + str(indices[minRecommended[idx][1]]) + " Minuten"
    print(returnStr)
    return returnStr


def getMinutely(minData):
    # requires ["minutely"] key from base data set
    dt = [d["dt"] for d in minData]
    prec = [d["precipitation"] for d in minData]
    minutely = [dt, prec]
    return minutely