from __future__ import division
import gpsTools as gps
from math import floor
import numpy as np
from sklearn.cluster import DBSCAN

def getmedianclustersize(clusters):
    n = []
    for cluster in clusters:
        n.append(len(cluster))
    return floor(np.median(n))

def getdistance(gps_coord, all_coords):
    return [gps.getdistanceinkm(gps_coord, all_coords[i]) for i in range(len(all_coords))]

def getclusters(gps_coords, second_pass = False, max_dist_in_meters=20, min_no_samples = 3, median_cluster_size = 5):
    final_clusters = {}
    final_clusters['sc'] = []
    final_clusters['nz'] = []
    n = len(gps_coords)
    if min_no_samples > n:
        final_clusters = None
    else:
        for gps_coord  in gps_coords:
            distance_row = getdistance(gps_coord, gps_coords)
            less_than_max = []
            for distance in distance_row:
                less_than_max.append(1 if distance <= max_dist_in_meters/1000 else 0)
            if second_pass:
                median_cluster_size = 5 if median_cluster_size > 5 else median_cluster_size
                if sum(less_than_max) >= median_cluster_size:
                    final_clusters['sc'].append(gps_coord)
                else:
                    final_clusters['nz'].append(gps_coord)
            else:
                if sum(less_than_max) >= floor(n/2):
                    final_clusters['sc'].append(gps_coord)
                else:
                    final_clusters['nz'].append(gps_coord)
    return final_clusters

def intersectingclusters(all_clusters):
    n = len(all_clusters)
    to_merge_with = np.zeros((n,n))
    to_merge_with = to_merge_with.tolist()
    for i in range(n):
        hull1 = gps.getconvexhull(all_clusters[i])
        for j in range(n):
            if i == j:
                continue
            hull2 = gps.getconvexhull(all_clusters[j])
            to_merge_with[i][j] = 1 if gps.dohullsintersect(hull1, hull2) else 0
    return to_merge_with

def mergeclusters(all_clusters, to_merge_with):
    merged_clusters = []
    n = len(all_clusters)
    worked_with = [0 for idx in range(n)]
    for i in range(n):
        disconnected_cluster = 0
        merged_cluster = []
        # if that particular cluster has not been looked at, select it, and check it with every other
        if 0 == worked_with[i]:
            merged_cluster = all_clusters[i]
            for j in range(n):
                if (1 == to_merge_with[i][j]) and (0 == worked_with[j]):
                    worked_with[i] = 1
                    worked_with[j] = 1
                    merged_cluster = merged_cluster + all_clusters[j]
                else:
                    disconnected_cluster += 1
            # if there were no clusters that intersected with this cluster
            if (0 == worked_with[i]) and (n == disconnected_cluster):
                worked_with[i] = 1
            # if the cluster has been worked on, add it to the merged clusters list
            if 1 == worked_with[i]:
                merged_clusters.append(merged_cluster)
        else:
            continue
    return merged_clusters

def getdbscanclusters(gps_coords, second_pass = False, max_dist_in_meters=20, min_no_samples = 3, median_cluster_size = 5):
    n = len(gps_coords)
    if min_no_samples > n:
        final_clusters = None
    else:
        distance_matrix = gps.getdistancematrix(gps_coords)
        if second_pass:
            min_no_samples = 5 if median_cluster_size > 5 else median_cluster_size
        db_obj = DBSCAN(eps=max_dist_in_meters/1000, min_samples=min_no_samples, metric= 'precomputed').fit(distance_matrix)
        cluster_idx = db_obj.labels_.tolist()
        cluster = {}
        assert len(cluster_idx) == len(gps_coords), "something is wrong, #cluster: "+str(len(cluster_idx))+", #coords: " \
                                                    + str(len(gps_coords))
        for idx in range(len(cluster_idx)):
            if cluster_idx[idx] not in cluster:
                cluster[cluster_idx[idx]] = []
            cluster[cluster_idx[idx]].append(gps_coords[idx])
        final_clusters = {}
        final_clusters['sc'] = []
        final_clusters['nz'] = []
        for key in cluster.keys():
            if not (-1 == key):
                final_clusters['sc'].append(cluster[key])
            else:
                final_clusters['nz'] = cluster[-1]
    return final_clusters