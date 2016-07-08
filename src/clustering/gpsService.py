import preprocessing as pr
import identifyTravel as travel
import identifyClusters as clusters
import gpsTools as gps
import collections
from GPSConstants import SurveyConstants
from GPSConstants import LocationContext

class gps_service:

    __pid = None
    __participant_data = None
    __travel_clusters = None
    __stationary_clusters = None
    __stationary_points = None
    __noise_markers = None
    __error_files = None
    __stationary_cluster_boundaries = None
    __internal_location_info = None
    __stationary_cluster_label = None

    def set_pid(self, pid):
        self.__pid = pid

    def set_participant_data(self, participant_data):
        self.__participant_data = participant_data

    def clean_house(self):
        self.__travel_clusters = []
        self.__stationary_clusters = []
        self.__stationary_points = []
        self.__noise_markers = []
        self.__pid = None
        self.__participant_data = None
        self.__error_files = 0
        self.__stationary_cluster_boundaries = []
        self.__internal_location_info = {}
        self.__stationary_cluster_label = []

    def get_travelling_and_stationary_clusters(self):
        '''
        for each data point within the participant data, distinguish between the travelling, and non-travelling data.
        Once all the travelling clusters, and non-travelling points have been extracted perform the DBSCAN clustering
        on the non-travelling points to obtain the stationary clusters, and noise markers.
        :return:
        '''
        for data_sample in self.__participant_data:
            try:
                self.__internal_location_info[(data_sample[SurveyConstants.PATIENT_ID],
                                               data_sample[SurveyConstants.CONDITION_ID],
                                               data_sample[SurveyConstants.SESSION_ID])] = \
                    LocationContext.LOCATION_CONTEXT_VALUES[data_sample[SurveyConstants.LOCATION_CONTEXT]]
                gps_coords_clean = pr.getcleangpsdata(data_sample[34], remove_duplicates=True,
                                                      pid=data_sample[0], cid=data_sample[1], sid=data_sample[2])
                if not gps_coords_clean:
                    continue
            except IOError:
                self.__error_files += 1
                continue
            # TODO: the speed limit has to be decided, are people walking also considered travelling?
            distances, speeds = travel.getalldistancesandspeeds(gps_coords_clean)
            travel_result = travel.istravelling(speeds, gps_coords_clean, selection_factor=0.7)
            if travel_result[0]:
                # travel_clusters.append(gps_coords_clean)
                if not 0 == len(travel_result[1]):
                    self.__travel_clusters.append(travel_result[1])
                if not 0 == len(travel_result[2]):
                    self.__stationary_points += travel_result[2]
            else:
                self.__stationary_points += gps_coords_clean
        eps_list = range(20, 51, 10)
        min_sample_list = [3, 5, 7]
        '''
        since all the stationary points are being collected for a given participants, the hull intersection functions
        never get called.
        '''
        print 'collected all points, clustering, eps_list:', eps_list, ', min_sample_list:', min_sample_list
        sc_nz = clusters.getdbscanclusters(self.__stationary_points, eps_list, min_sample_list)
        print 'done'
        if sc_nz is not None:
            if not ([] == sc_nz['sc']):
                self.__stationary_clusters = sc_nz['sc']
            if not ([] == sc_nz['nz']):
                self.__noise_markers = sc_nz['nz']
        print 'stationary clusters: ' + str(len(self.__stationary_clusters)) + ', travel clusters: ' + str(
            len(self.__travel_clusters))
        for cluster_points in self.__stationary_clusters:
            boundary_points = gps.getconvexhull(cluster_points)
            self.__stationary_cluster_boundaries.append(boundary_points)
            cluster_point_types = []
            for cluster_point in cluster_points:
                cluster_point_types.append(self.__internal_location_info[(cluster_point[-3],
                                                                          cluster_point[-2],
                                                                          cluster_point[-1])])
            label_counts = collections.Counter(cluster_point_types)
            most_common_label = label_counts.most_common(1)
            self.__stationary_cluster_label.append(most_common_label[0][0])
        return self.__travel_clusters, self.__stationary_clusters, self.__stationary_cluster_boundaries, \
               self.__stationary_cluster_label, self.__noise_markers, self.__error_files

    def __init__(self):
        pass
