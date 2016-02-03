import sys
import gpsTools as gps
import identifyTravel as travel
import identifyClusters as clusters
import createClusterPlot as plotcl
from copy import deepcopy
import basicDebug as bD

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

def main():
    print 'entered main'
    ipFile = sys.argv[1]
    template_start = sys.argv[2]
    template_end = sys.argv[3]
    rect_t = sys.argv[4]
    rect_s = sys.argv[5]
    marker_end = sys.argv[6]
    op_path = sys.argv[7]
    print 'arguments assigned variables'
    data = getAllData(ipFile)
    per_participant_data = getPerParticipantData(data)
    print 'per participant data extracted'
    participantList = per_participant_data.keys()
    print participantList
    for pid in participantList:
        print '\n\npid: '+ pid
        travel_clusters = []
        stationary_clusters = []
        noise_markers = []
        participant_data = per_participant_data[pid]
        errorFiles = 0
        for data_sample in participant_data:
            if '' is not data_sample[34]:
                try:
                    gC = gps.readgpsfile(data_sample[34])
                except IOError:
                    errorFiles += 1
                    continue
                distances, speeds = travel.getalldistancesandspeeds(gC)
                travel_result = travel.istravelling(speeds, gC)
                if travel_result[0]:
                    travel_clusters.append(gC)
                else:
                    sc_nz = clusters.getclusters(gC)
                    if sc_nz is not None:
                        if not([] == sc_nz['sc']):
                            stationary_clusters.append(sc_nz['sc'])
                        if not([] == sc_nz['nz']):
                            noise_markers += sc_nz['nz']
        temp_noise_markers = noise_markers
        median_cluster_size = clusters.getmedianclustersize(stationary_clusters)
        sc_nz = clusters.getclusters(temp_noise_markers, second_pass= True, median_cluster_size = median_cluster_size)
        if sc_nz is not None:
            if not([] == sc_nz['sc']):
                stationary_clusters.append(sc_nz['sc'])
            if not([] == sc_nz['nz']):
                noise_markers = sc_nz['nz']
        print 'second pass, original # nz: ' + str(len(temp_noise_markers)) + \
              ' new # nz: ' + str(len(noise_markers)) + \
              ' median cluster size: ' + str(median_cluster_size)
        '''
        for idx in range(len(stationary_clusters)):
            stationary_clusters[idx] = gps.uniquevaluesincluster(stationary_clusters[idx])
        try:
            stationary_clusters.remove([])
        except ValueError:
            pass
        returned_cluster_len = 0
        merged_clusters = deepcopy(stationary_clusters)
        print 'merging clusters'
        while not (returned_cluster_len == len(merged_clusters)):
            to_merge_with = clusters.intersectingclusters(merged_clusters)
            merged_clusters = clusters.mergeclusters(merged_clusters, to_merge_with)
            returned_cluster_len = len(merged_clusters)
            print 'returned cluster no: ' + str(returned_cluster_len)
        stationary_clusters = merged_clusters
        '''
        bD.writecluster(pid, stationary_clusters)
        print 'writing clusters, done'
        plotcl.createclusterplot(op_path + '/' + pid + '.html', stationary_clusters, travel_clusters, noise_markers, rect_t, rect_s, marker_end, template_start, template_end)
        print 'plotted'
        print 'there was an error openeing a few files, total number :' + str(errorFiles)

if __name__ == "__main__":
    if not (8 == len(sys.argv)):
        print 'Usage: python runMe.py <survey file (csv)> <template_start> <template_end> <rectangle_stationary> <rectangle_travel> <marker_end> <op path>'
    else:
        main()