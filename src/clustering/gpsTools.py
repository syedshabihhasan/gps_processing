from __future__ import division
from math import radians, sin, cos, atan2, sqrt
from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay
from shapely.geometry import Polygon


def getspeedperhour(distance_travelled, time_in_seconds):
    return distance_travelled / (time_in_seconds / 3600)


def getdistanceinkm(start_coord, end_coord):
    r = 6373
    del_lat = radians(end_coord[0] - start_coord[0])
    del_lon = radians(end_coord[1] - start_coord[1])
    a = sin(del_lat / 2) ** 2 + \
        cos(radians(start_coord[0])) * cos(radians(end_coord[0])) * \
        sin(del_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return r * c


def getdistanceandspeed(start_coord, end_coord, sampling_rate):
    distance = getdistanceinkm(start_coord, end_coord)
    speed = getspeedperhour(distance, 1 / sampling_rate)
    return distance, speed


def getboundary(all_coord):
    min_lat = float(1000)
    min_lon = float(1000)
    max_lat = float(-1000)
    max_lon = float(-1000)
    for coord in all_coord:
        lat = coord[0]
        lon = coord[1]
        if lat <= min_lat:
            min_lat = lat
        elif lat >= max_lat:
            max_lat = lat
        elif lon <= min_lon:
            min_lon = lon
        elif lon >= max_lon:
            max_lon = lon
        else:
            continue
    return [min_lat, min_lon], [max_lat, max_lon]


def check_polygon_membership(cluster_boundary, points_to_check):
    cluster_boundary_points = [[x[0], x[1]] for x in cluster_boundary]
    hull = cluster_boundary_points
    if not isinstance(hull, Delaunay):
        hull = Delaunay(hull)
    gps_coords_to_check = [[x[0], x[1]] for x in points_to_check]
    point_in_cluster = []
    for coord in gps_coords_to_check:
        point_in_cluster.append(1 if hull.find_simplex(coord) >= 0 else 0)
    return point_in_cluster


def check_polygon_memberships(cluster_boundaries, points_to_check):
    cluster_decisions = []
    for cluster_boundary in cluster_boundaries:
        cluster_decisions.append(check_polygon_membership(cluster_boundary, points_to_check))
    return cluster_decisions


def getconvexhull(all_coord):
    coords_to_use = []
    for coord in all_coord:
        coords_to_use.append([coord[0], coord[1]])
    try:
        hull = ConvexHull(coords_to_use)
    except:
        # print 'An error occured: ', sys.exc_info()[0]
        print 'all_coords:', all_coord
        print 'coords_to_use: ', coords_to_use
        raise
    boundary_vertices_idx = list(hull.vertices)
    boundary_vertices = []
    for idx in boundary_vertices_idx:
        boundary_vertices.append(all_coord[idx])
    return boundary_vertices


def readgpsfile(filename, ignore_accuracy=True):
    with open(filename, 'r') as f:
        data = f.read()
    gps_coords = data.splitlines()
    try:
        gps_coords.remove('')
    except ValueError:
        pass
    final_coords = []
    for gps_coord in gps_coords:
        gps_coord = gps_coord.split(',')
        if ignore_accuracy:
            final_coords.append([float(gps_coord[1]), float(gps_coord[0])])
        else:
            final_coords.append([float(gps_coord[1]), float(gps_coord[0]), float(gps_coord[2])])
    return final_coords


def dohullsintersect(hull1_coord, hull2_coord):
    hull1 = []
    hull2 = []
    for coord in hull1_coord:
        hull1.append([coord[0], coord[1]])
    for coord in hull2_coord:
        hull2.append([coord[0], coord[1]])
    hull1 = Polygon(hull1)
    hull2 = Polygon(hull2)
    return hull1.intersects(hull2)


def uniquevaluesincluster(cluster_coords):
    coord_tuples = []
    for coord in cluster_coords:
        coord_tuples.append((coord[0], coord[1]))
    coord_set = set(coord_tuples)
    coord_set = list(coord_set)
    for coord in coord_set:
        coord_tuples.append([coord[0], coord[1]])
    if 3 <= len(coord_tuples):
        return coord_tuples
    else:
        return []


def getdistancematrix(coords):
    dist_matrix = []
    for i in range(len(coords)):
        temp = [0.0] * len(coords)
        for j in range(len(coords)):
            if j == i:
                break
            else:
                temp[j] = getdistanceinkm(coords[i], coords[j]) * 1000.0
                dist_matrix[j][i] = temp[j]
        dist_matrix.append(temp)
    return dist_matrix
