import gpsTools as gps

def createPolygon(cluster_points, cluster_no):
    try:
        boundary_vertices = gps.getconvexhull(cluster_points)
    except:
        print 'There was an error trying to get the hull for cluster no. '+ str(cluster_no)+', skipping'
        return ''
    toWrite = 'var cluster_' + str(cluster_no) + ' = [\n'
    for vertex in boundary_vertices:
        toWrite += '{lat:' + str(vertex[0]) + ', lng:' + str(vertex[1]) + '},\n'
    toWrite += '];\n\n'
    toWrite += "var cluster_" + str(cluster_no) + "_c = new google.maps.Polygon({\n" \
               "paths: cluster_" + str(cluster_no) + ", \n " \
               "strokeColor: '#00FF00', \n" \
               "strokeOpacity: 0.8, \n" \
               "strokeWeight: 2, \n" \
               "fillColor: '#00FF00', \n" \
               "fillOpacity: 0.35\n});\ncluster_"+str(cluster_no) + "_c.setMap(map);\n\n"
    return toWrite

def readtemplatefile(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data

def gettexts(template_start, template_end, rectangle_t_script, rectangle_s_script, marker_javascript):
    return readtemplatefile(template_start), readtemplatefile(template_end), readtemplatefile(rectangle_t_script), readtemplatefile(rectangle_s_script), readtemplatefile(marker_javascript)

def createclusterplot(path_to_use, stationary_clusters, travel_clusters, noise_markers, rectangle_t_script, rectangle_s_script, marker_javascript, template_start, template_end):
    start_txt, end_txt, rectangle_t_txt, rectangle_s_txt, marker_txt = gettexts(template_start, template_end, rectangle_t_script, rectangle_s_script, marker_javascript)
    stationary_full_text = ''
    markers_stationary_info = '\nvar markers_stationary_info = ['
    markers_stationary = '\nvar markers_stationary = ['
    idx = 0
    for cluster in stationary_clusters:
        stationary_full_text += createPolygon(cluster, idx)
        idx += 1
        for coord in cluster:
            markers_stationary += '[' + str(coord[0]) + ',' + str(coord[1]) + '], \n'
            markers_stationary_info += "'"+str(coord[2])+","+str(coord[3])+","+str(coord[4])+"',\n"
    markers_stationary += '];\n'
    markers_stationary_info += "];\n"
    #markers_stationary = stationary_full_text

    travel_full_text = ''
    markers_travel = '\nvar markers_travel = ['
    markers_travel_info = '\nvar markers_travel_info = ['
    for cluster in travel_clusters:
        min_coord, max_coord = gps.getboundary(cluster)
        to_insert = 'north: ' + str(min_coord[0]) + ', \n west: '+ str(min_coord[1]) + ', \n' \
                    ' south: ' + str(max_coord[0]) + ', \n east: '+ str(max_coord[1]) + '\n }\n});'
        travel_full_text += 'var rect'+str(idx)+'=' + rectangle_t_txt + to_insert + '\n'
        idx += 1
        for coord in cluster:
            markers_travel += '[' + str(coord[0]) + ',' + str(coord[1]) + '], \n'
            markers_travel_info += "'"+str(coord[2])+","+str(coord[3])+","+str(coord[4])+"',\n"
    markers_travel += '];\n'
    markers_travel_info += '];\n'

    markers_full_text = 'var markers = ['
    markers_full_text_info = '\nvar markers_info = ['
    for marker in noise_markers:
        markers_full_text += '[' + str(marker[0]) + ', ' + str(marker[1]) + '], \n'
        markers_full_text_info += "'"+str(marker[2])+","+str(marker[3])+","+str(marker[4])+"',\n"
    markers_full_text_info += '];\n'
    markers_full_text += '];\n' + markers_full_text_info + markers_travel_info + markers_stationary_info + \
                         markers_stationary + markers_travel + marker_txt

    #final_txt = start_txt + stationary_full_text + travel_full_text + markers_full_text + end_txt
    final_txt = start_txt + stationary_full_text + markers_full_text + end_txt
    f = open(path_to_use, 'w')
    f.write(final_txt)
    f.close()

