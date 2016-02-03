import gpsTools as gps

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

def getcleangpsdata(filename, accuracy_threshold = 100):
    gC = gps.readgpsfile(filename, False)
    within_range_gps = []
    # find all coordinates within the accuracy threshold
    for coord in gC:
        if accuracy_threshold >= coord[2]:
            within_range_gps.append((coord[0], coord[1]))
    # remove duplicates
    within_range_gps = list(set(within_range_gps))
    if 1 >= len(within_range_gps):
        return []
    else:
        for idx in range(len(within_range_gps)):
            within_range_gps[idx] = [within_range_gps[idx][0], within_range_gps[idx][1]]
        return within_range_gps