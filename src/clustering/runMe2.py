from GPSConstants import SurveyConstants
from GPSConstants import LocationContext
import preprocessing as pr
import argparse
from gpsService import gps_service
import gpsTools as gps
from glob import glob
import pickle
import basicDebug as bD

def main():
    print 'now entered main'

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '-I', help='input CSV file', required=True)
    parser.add_argument('-o', '-O', help='output path', required=True)
    parser.add_argument('-c', '-C', help='cluster data path', required=False)

    args = parser.parse_args()

    input_file = args.i
    output_path = args.o
    cluster_data_path = args.c

    cluster_service = gps_service()

    print 'arguments assigned variables'
    data = pr.getAllData(input_file)
    print 'keeping only app init and live listening'
    data_to_use = pr.filtersurveydata(data, SurveyConstants.CONDITION_ID, ['1', '2', '3', '4'])
    cluster_data_files = glob(cluster_data_path + '*.data')
    app_init_data = pr.filtersurveydata(data_to_use, SurveyConstants.USER_INITIATED, ['false'])
    listening_data = pr.filtersurveydata(data_to_use, SurveyConstants.LISTENING, ['true'])
    data = app_init_data + listening_data
    print 'done'
    per_participant_data = pr.getPerParticipantData(data)
    print 'per participant data extracted'
    participant_list = per_participant_data.keys()
    print participant_list
    min_data_sample_no = 5
    final_result = {}
    cluster_results = {}
    for pid in participant_list:
        print '\n\npid: ' + pid
        if len(per_participant_data[pid]) < min_data_sample_no:
            print '# of samples < min_data_sample_no (' + str(min_data_sample_no) + '), skipping pid'
            continue
        if cluster_data_path + pid + '_all_data.data' not in cluster_data_files:
            print 'could not find data file for pid: ', pid, ', skipping'
            continue
        final_result[pid] = {}
        cluster_results[pid] = {}
        cluster_service.clean_house()
        cluster_service.set_pid(pid)
        cluster_service.set_participant_data(per_participant_data[pid])
        with open(cluster_data_path+pid+'_all_data.data', 'rb') as f:
            data_dict = pickle.load(f)
            cluster_boundaries = data_dict['boundary']
            cluster_labels = data_dict['label']
        for data_sample in per_participant_data[pid]:
            n_pid = data_sample[SurveyConstants.PATIENT_ID]
            cid = data_sample[SurveyConstants.CONDITION_ID]
            sid = data_sample[SurveyConstants.SESSION_ID]
            if '' == data_sample[SurveyConstants.GPS_PATH]:
                print 'empty gps file path, skipping \n', data_sample
                continue
            gps_coords_clean = pr.getcleangpsdata(data_sample[SurveyConstants.GPS_PATH], remove_duplicates=True,
                                                  pid=n_pid, cid=cid, sid=sid)
            if gps_coords_clean is None:
                print 'no GPS data for ', n_pid, cid, sid, ', skipping'
                continue
            travel_result = cluster_service.find_travelling(gps_coords_clean)
            final_result[pid][(n_pid, cid, sid)] = \
                [(LocationContext.LOCATION_CONTEXT_VALUES[data_sample[SurveyConstants.LOCATION_CONTEXT]],
                  len(gps_coords_clean))]
            cluster_results[pid][(n_pid, cid, sid)] = [
                (LocationContext.LOCATION_CONTEXT_VALUES[data_sample[SurveyConstants.LOCATION_CONTEXT]],
                 gps_coords_clean)]
            if travel_result[0]:
                if not 0 == len(travel_result[1]):
                    final_result[pid][(n_pid, cid, sid)].append(('Travel', len(travel_result[1])))
                    cluster_results[pid][(n_pid, cid, sid)].append(('Travel', (travel_result[1])))
                if not 0 == len(travel_result[2]):
                    cluster_decisions = gps.check_polygon_memberships(cluster_boundaries, travel_result[2])
                    cluster_vals = [sum(x) for x in cluster_decisions]
                    for idx in range(len(cluster_vals)):
                        if not 0 == cluster_vals[idx]:
                            final_result[pid][(n_pid, cid, sid)].append((cluster_labels[idx], cluster_vals[idx]))
                            cluster_results[pid][(n_pid, cid, sid)].append((cluster_labels[idx], travel_result[2],
                                                                            cluster_decisions[idx]))
    bD.write_variable(final_result, 'count_result', output_path)
    bD.write_variable(cluster_results, 'cluster_results', output_path)
        # TODO: 1: read the pid's data file,
        # TODO: 2.1: for each new file get extract the label from the survey,
        # TODO: 2.2: check whether the person is travelling, or stationary, if stationary check for
        # membership within older clusters
        # TODO: 2.3: create confusion matrix, save individual results

if __name__ == "__main__":
    main()
