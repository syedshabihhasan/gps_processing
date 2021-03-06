from __future__ import division
import gpsTools as gps
from math import floor


def getalldistancesandspeeds(gps_coords, sampling_rate=0.1):
    distances = []
    speeds = []
    if 1 < len(gps_coords):
        n = len(gps_coords)
        for idx in range(1, n):
            dist, sp = gps.getdistanceandspeed(gps_coords[idx - 1], gps_coords[idx], sampling_rate)
            distances.append(dist)
            speeds.append(sp)
    else:
        distances = [-1, -1]
        speeds = [-1, -1]
    return distances, speeds


def istravelling(speeds, gps_coords, speed_limit=5, selection_factor=0.5):
    if -1 == speeds[0] or 2 > len(speeds):
        return [False, 0]
    is_above_limit = []
    travelling_clusters = []
    not_travelling_clusters = []
    for idx in range(len(speeds)):
        is_above_limit.append(1 if speeds[idx] > speed_limit else 0)
        if speed_limit < speeds[idx]:
            if 0 == idx:
                travelling_clusters.append(gps_coords[0])
                travelling_clusters.append(gps_coords[1])
            else:
                travelling_clusters.append(gps_coords[idx + 1])
        else:
            if 0 == idx:
                not_travelling_clusters.append(gps_coords[0])
                not_travelling_clusters.append(gps_coords[1])
            else:
                not_travelling_clusters.append(gps_coords[idx + 1])
    # return [True, gps.getboundary(gps_coords)] if sum(is_above_limit) >= floor((len(speeds) - 1) * selection_factor) \
    #     else [False, 0]
    return [True, travelling_clusters, not_travelling_clusters]
