from GPSConstants import SurveyConstants
import createClusterPlot as plotcl
import basicDebug as bD
import preprocessing as pr
import argparse
from gpsService import gps_service


def main():
    print 'now entered main'

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '-I', help='input CSV file', required=True)
    parser.add_argument('-ts', '-TS', help='template start', required=True)
    parser.add_argument('-te', '-TE', help='template end', required=True)
    parser.add_argument('-rs', '-RS', help='rectangle stationary', required=True)
    parser.add_argument('-rt', '-RT', help='rectangle travel', required=True)
    parser.add_argument('-me', '-ME', help='marker end', required=True)
    parser.add_argument('-o', '-O', help='output path', required=True)

    args = parser.parse_args()

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
    data_to_use = pr.filtersurveydata(data, SurveyConstants.CONDITION_ID, ['99', '5', '6'])
    app_init_data = pr.filtersurveydata(data_to_use, SurveyConstants.USER_INITIATED, ['false'])
    listening_data = pr.filtersurveydata(data_to_use, SurveyConstants.LISTENING, ['true'])
    data = app_init_data + listening_data
    print 'done'
    per_participant_data = pr.getPerParticipantData(data)
    print 'per participant data extracted'
    participant_list = per_participant_data.keys()
    print participant_list
    min_data_sample_no = 5
    for pid in participant_list:
        print '\n\npid: ' + pid
        if len(per_participant_data[pid]) < min_data_sample_no:
            print '# of samples < min_data_sample_no (' + str(min_data_sample_no) + '), skipping pid'
            continue
        cluster_service.clean_house()
        cluster_service.set_pid(pid)
        cluster_service.set_participant_data(per_participant_data[pid])
        travel_clusters, stationary_clusters, stationary_cluster_boundaries, stationary_cluster_labels, \
        noise_markers, error_files, stationary_points = cluster_service.get_travelling_and_stationary_clusters()
        # bD.writecluster(pid, stationary_clusters, output_path, 'S', stationary_cluster_labels)
        # bD.writecluster(pid, noise_markers, output_path, 'N')
        # bD.writecluster(pid, travel_clusters, output_path, 'T')
        # bD.write_variable([stationary_cluster_boundaries, stationary_cluster_labels],
        #                   pid + '_cluster_boundary_label.data', output_path)
        bD.write_variable({'travel': travel_clusters,
                           'stationary': stationary_clusters,
                           'boundary': stationary_cluster_boundaries,
                           'label': stationary_cluster_labels,
                           'noise': noise_markers,
                           'points': stationary_points,
                           'data': per_participant_data[pid]}, pid+'_all_data.data', output_path)
        print 'writing clusters, done'
        plotcl.createclusterplot(output_path + '/' + pid + '.html', stationary_clusters, travel_clusters,
                                 noise_markers, rectangle_travel, rectangle_stationary, marker_end,
                                 template_start, template_end, stationary_cluster_labels)
        print 'plotted'
        print 'there was an error opening a few files, total number :' + str(error_files)


if __name__ == "__main__":
    main()
