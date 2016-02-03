import sys

__author__ = 'hasanshabih'

def getAllData(ipFile):
    f = open(ipFile, 'r')
    data = f.read()
    f.close()

    data = data.split('\r')
    data.pop(0)
    try:
        data.remove('')
    except ValueError:
        pass

    sanitizedData = []
    for dataSample in data:
        sanitizedData.append(dataSample.split(','))
    return sanitizedData

def getPerParticipantData(data):
    perParticipantDict = {}
    for dataSample in data:
        pid = dataSample[0]
        if not perParticipantDict.has_key(pid):
            perParticipantDict[pid] = []
        perParticipantDict[pid].append(dataSample)
    return perParticipantDict

def getTemplateText(templateStart, templateEnd):
    f = open(templateStart, 'r')
    tStart = f.read()
    f.close()

    f = open(templateEnd, 'r')
    tEnd = f.read()
    f.close()

    return tStart, tEnd

def plotPerParticipant(data, opFolder, templateStart, templateEnd):
    participantList = data.keys()
    tStart, tEnd = getTemplateText(templateStart, templateEnd)
    for pid in participantList:
        participantData = data[pid]
        locationText = ''
        for dataSample in participantData:
            if '' is not dataSample[34]:
                try:
                    f = open(dataSample[34])
                    gpsData = f.read().splitlines()
                    f.close()
                except IOError:
                    print 'Error occured!'
                    print dataSample
                if not(0 == len(gpsData)):
                    for coord in gpsData:
                        coord = coord.split(',')
                        locationText += '[' + coord[1] + ',' + coord[0] + '],\n'
        f = open(opFolder+'/'+pid+'.html', 'w')
        toPut = tStart + locationText + tEnd
        f.write(toPut)
        f.close()

def main(ipFile, opFolder, templateStart, templateEnd):
    allSurveyData = getAllData(ipFile)
    perParticipantData = getPerParticipantData(allSurveyData)
    plotPerParticipant(perParticipantData, opFolder, templateStart, templateEnd)
    return

if __name__ == "__main__":
    if not(5 == len(sys.argv)):
        print 'Usage: python createPlot.py <inputFile (csv)> <output folder without trailing /> ' \
              '<template start> <template end>'
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])