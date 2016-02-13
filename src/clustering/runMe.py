import sys
import identifyTravel as travel
import identifyClusters as clusters
import createClusterPlot as plotcl
from copy import deepcopy
import basicDebug as bD
import preprocessing as pr


def main():
    print 'now entered main'
    ipFile = sys.argv[1]
    template_start = sys.argv[2]
    template_end = sys.argv[3]
    rect_t = sys.argv[4]
    rect_s = sys.argv[5]
    marker_end = sys.argv[6]
    op_path = sys.argv[7]
    print 'arguments assigned variables'
    data = pr.getAllData(ipFile)
    print 'keeping only app init and live listening'
    app_init_data = pr.filtersurveydata(data, 33, ['false'])
    listening_data = pr.filtersurveydata(data, 7, ['true'])
    data = app_init_data + listening_data
    print 'done'
    per_participant_data = pr.getPerParticipantData(data)
    print 'per participant data extracted'
    participantList = per_participant_data.keys()
    print participantList
    for pid in participantList:
        print '\n\npid: '+ pid
        travel_clusters = []
        stationary_clusters = []
        stationary_points = []
        noise_markers = []
        participant_data = per_participant_data[pid]
        errorFiles = 0
        for data_sample in participant_data:
            try:
                gC = pr.getcleangpsdata(data_sample[34], remove_duplicates=True, pid=data_sample[0], cid=data_sample[1], sid=data_sample[2])
                if [] == gC:
                    continue
            except IOError:
                errorFiles += 1
                continue
            distances, speeds = travel.getalldistancesandspeeds(gC)
            travel_result = travel.istravelling(speeds, gC, selection_factor=0.95)
            if travel_result[0]:
                travel_clusters.append(gC)
            else:
                stationary_points += gC
        #         sc_nz = clusters.getdbscanclusters(gC)
        #         if sc_nz is not None:
        #             if not([] == sc_nz['sc']):
        #                 #stationary_clusters.append(sc_nz['sc'])
        #                 temp_cls = sc_nz['sc']
        #                 for cls in temp_cls:
        #                     stationary_clusters.append(cls)
        #             if not([] == sc_nz['nz']):
        #                 noise_markers += sc_nz['nz']
        # temp_noise_markers = noise_markers
        # median_cluster_size = clusters.getmedianclustersize(stationary_clusters)
        # sc_nz = clusters.getdbscanclusters(temp_noise_markers, second_pass= True, median_cluster_size = median_cluster_size)
        print 'collected all points, clustering'
        sc_nz = clusters.getdbscanclusters(stationary_points)
        print 'done'
        # if sc_nz is not None:
        #     if not([] == sc_nz['sc']):
        #         #stationary_clusters.append(sc_nz['sc'])
        #         temp_cls = sc_nz['sc']
        #         for cls in temp_cls:
        #             stationary_clusters.append(cls)
        #     if not([] == sc_nz['nz']):
        #         noise_markers = sc_nz['nz']
        # print 'second pass, original # nz: ' + str(len(temp_noise_markers)) + \
        #       ' new # nz: ' + str(len(noise_markers)) + \
        #       ' median cluster size: ' + str(median_cluster_size)
        # print 'Looking at merging clusters'
        # stationary_clusters = pr.removesinglevalues(stationary_clusters, less_than=4)
        # returned_cluster_len = len(stationary_clusters)
        # last_cluster_len = -1
        # merged_clusters = deepcopy(stationary_clusters)
        # print 'merging clusters'
        # firstpass = True
        # old_clusters = []
        # while not (returned_cluster_len == last_cluster_len):
        #     old_clusters = merged_clusters
        #     if firstpass:
        #         firstpass = False
        #         last_cluster_len = len(merged_clusters)
        #         merged_clusters = pr.removesinglevalues(merged_clusters, less_than=4)
        #     else:
        #         last_cluster_len = returned_cluster_len
        #     to_merge_with = clusters.intersectingclusters(merged_clusters)
        #     merged_clusters = clusters.mergeclusters(merged_clusters, to_merge_with)
        #     returned_cluster_len = len(merged_clusters)
        #     print 'returned cluster len: ' + str(returned_cluster_len) + ' last cluster len: ' + str(last_cluster_len)
        # stationary_clusters = merged_clusters
        if sc_nz is not None:
            if not ([] == sc_nz['sc']):
                stationary_clusters = sc_nz['sc']
            if not ([] == sc_nz['nz']):
                noise_markers = sc_nz['nz']
        print 'stationary clusters: ' + str(len(stationary_clusters)) + ', travel clusters: ' + str(len(travel_clusters))
        bD.writecluster(pid, stationary_clusters, 'S')
        bD.writecluster(pid, noise_markers, 'N')
        bD.writecluster(pid, travel_clusters, 'T')
        print 'writing clusters, done'
        plotcl.createclusterplot(op_path + '/' + pid + '.html', stationary_clusters, travel_clusters, noise_markers, rect_t, rect_s, marker_end, template_start, template_end)
        print 'plotted'
        print 'there was an error openeing a few files, total number :' + str(errorFiles)

if __name__ == "__main__":
    if not (8 == len(sys.argv)):
        print 'Usage: python runMe.py <survey file (csv)> <template_start> <template_end> <rectangle_stationary> <rectangle_travel> <marker_end> <op path>'
    else:
        main()