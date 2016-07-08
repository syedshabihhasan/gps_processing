from GPSConstants import SurveyConstants
import identifyTravel as travel
import identifyClusters as clusters
import createClusterPlot as plotcl
import basicDebug as bD
import preprocessing as pr
import argparse
from gpsService import gps_service


def main():
    print 'now entered main'

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '-I', help='input CSV file')
    parser.add_argument('-ts', '-TS', help='template start')
    parser.add_argument('-te', '-TE', help='template end')
    parser.add_argument('-rs', '-RS', help='rectangle stationary')
    parser.add_argument('-rt', '-RT', help='rectangle travel')
    parser.add_argument('-me', '-ME', help='marker end')
    parser.add_argument('-o', '-O', help='output path')

    args = parser.parse_args()

    # input_file = sys.argv[1]
    # template_start = sys.argv[2]
    # template_end = sys.argv[3]
    # rectangle_travel = sys.argv[4]
    # rectangle_stationary = sys.argv[5]
    # marker_end = sys.argv[6]
    # output_path = sys.argv[7]

    input_file = args.i
    template_start = args.ts
    template_end = args.te
    rectangle_travel = args.rt
    rectangle_stationary = args.rs
    marker_end = args.me
    output_path = args.o

    cluster_service = gps_service()

    print 'arguments assigned variables'
    data = pr.getAllData(input_file)
    print 'keeping only app init and live listening'
    app_init_data = pr.filtersurveydata(data, SurveyConstants.USER_INITIATED, ['false'])
    listening_data = pr.filtersurveydata(data, SurveyConstants.LISTENING, ['true'])
    data = app_init_data + listening_data
    print 'done'
    per_participant_data = pr.getPerParticipantData(data)
    print 'per participant data extracted'
    participant_list = per_participant_data.keys()
    print participant_list
    for pid in participant_list:
        print '\n\npid: ' + pid
        cluster_service.clean_house()
        cluster_service.set_pid(pid)
        cluster_service.set_participant_data(per_participant_data[pid])
        travel_clusters, stationary_clusters, stationary_cluster_boundaries, \
        stationary_cluster_labels, noise_markers, errorFiles = cluster_service.get_travelling_and_stationary_clusters()
        # travel_clusters = []
        # stationary_clusters = []
        # stationary_points = []
        # noise_markers = []
        # participant_data = per_participant_data[pid]
        # errorFiles = 0
        # for data_sample in participant_data:
        #     try:
        #         gps_coords_clean = pr.getcleangpsdata(data_sample[34], remove_duplicates=True,
        #                                               pid=data_sample[0], cid=data_sample[1], sid=data_sample[2])
        #         if not gps_coords_clean:
        #             continue
        #     except IOError:
        #         errorFiles += 1
        #         continue
        #     # TODO: the speed limit has to be decided, are people walking also considered traveling?
        #     distances, speeds = travel.getalldistancesandspeeds(gps_coords_clean)
        #     travel_result = travel.istravelling(speeds, gps_coords_clean, selection_factor=0.7)
        #     if travel_result[0]:
        #         # travel_clusters.append(gps_coords_clean)
        #         if not 0 == len(travel_result[1]):
        #             travel_clusters.append(travel_result[1])
        #         if not 0 == len(travel_result[2]):
        #             stationary_points += travel_result[2]
        #     else:
        #         stationary_points += gps_coords_clean
        # eps_list = range(20, 51, 10)
        # min_sample_list = [3, 5, 7]
        # '''
        # since all the stationary points are being collected for a given participants, the hull intersection functions
        # never get called.
        # '''
        # print 'collected all points, clustering, eps_list:', eps_list, ', min_sample_list:', min_sample_list
        # sc_nz = clusters.getdbscanclusters(stationary_points, eps_list, min_sample_list)
        # print 'done'
        # if sc_nz is not None:
        #     if not ([] == sc_nz['sc']):
        #         stationary_clusters = sc_nz['sc']
        #     if not ([] == sc_nz['nz']):
        #         noise_markers = sc_nz['nz']
        # print 'stationary clusters: ' + str(len(stationary_clusters)) + ', travel clusters: ' + str(
        #     len(travel_clusters))
        bD.writecluster(pid, stationary_clusters, output_path, 'S', stationary_cluster_labels)
        bD.writecluster(pid, noise_markers, output_path, 'N')
        bD.writecluster(pid, travel_clusters, output_path, 'T')
        print 'writing clusters, done'
        plotcl.createclusterplot(output_path + '/' + pid + '.html', stationary_clusters, travel_clusters, noise_markers,
                                 rectangle_travel, rectangle_stationary, marker_end, template_start, template_end,
                                 stationary_cluster_labels)
        print 'plotted'
        print 'there was an error opening a few files, total number :' + str(errorFiles)


if __name__ == "__main__":
    main()
