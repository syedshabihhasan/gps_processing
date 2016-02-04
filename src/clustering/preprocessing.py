import gpsTools as gps

def getAllData(ipFile):
    f = open(ipFile, 'r')
    data = f.read()
    f.close()

    data = data.split('\r')
    titles = data.pop(0)
    titles = titles.split(',')
    for idx in range(len(titles)):
        print str(idx) + ':' + titles[idx]
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

def getcleangpsdata(filename, accuracy_threshold = 500, remove_duplicates = True, pid = 'EMA999', cid = '99', sid = '9999'):
    gC = gps.readgpsfile(filename, False)
    within_range_gps = []
    # find all coordinates within the accuracy threshold
    for coord in gC:
        if accuracy_threshold >= coord[2]:
            within_range_gps.append((coord[0], coord[1]))
    # remove duplicates
    if remove_duplicates:
        within_range_gps = list(set(within_range_gps))
    if 1 >= len(within_range_gps):
        return []
    else:
        for idx in range(len(within_range_gps)):
            within_range_gps[idx] = [within_range_gps[idx][0], within_range_gps[idx][1], pid, cid, sid]
        return within_range_gps

def filtersurveydata(survey_data, idx_to_filter_by, values_to_keep):
    survey_to_keep = []
    for sample in survey_data:
        if sample[idx_to_filter_by] in values_to_keep:
            survey_to_keep.append(sample)
    return survey_to_keep

def removesinglevalues(clusters, less_than = 2):
    n = range(len(clusters))
    to_remove = []
    for idx in n:
        if less_than > len(clusters[idx]):
            to_remove.append(idx)
    for idx in to_remove:
        try:
            del clusters[idx]
        except IndexError:
            pass
    print 'removed ' + str(len(to_remove)) + ' single values stationary clusters'
    return clusters

