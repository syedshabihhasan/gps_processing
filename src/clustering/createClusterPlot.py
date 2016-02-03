import gpsTools as gps

def readtemplatefile(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data

def gettexts(template_start, template_end, rectangle_t_script, rectangle_s_script, marker_javascript):
    return readtemplatefile(template_start), readtemplatefile(template_end), readtemplatefile(rectangle_t_script), readtemplatefile(rectangle_s_script), readtemplatefile(marker_javascript)

def createclusterplot(path_to_use, stationary_clusters, travel_clusters, noise_markers, rectangle_t_script, rectangle_s_script, marker_javascript, template_start, template_end):
    start_txt, end_txt, rectangle_t_txt, rectangle_s_txt, marker_txt = gettexts(template_start, template_end, rectangle_t_script, rectangle_s_script, marker_javascript)
    stationary_full_text = ''
    markers_stationary = '\nvar markers_stationary = ['
    idx = 0
    for cluster in stationary_clusters:
        min_coord, max_coord = gps.getboundary(cluster)
        to_insert = 'north: ' + str(min_coord[0]) + ', \n west: '+ str(min_coord[1]) + ', \n' \
                    ' south: ' + str(max_coord[0]) + ', \n east: '+ str(max_coord[1]) + '\n }\n});'
        stationary_full_text += 'var rect'+str(idx)+'=' + rectangle_s_txt + to_insert + '\n'
        idx += 1
        for coord in cluster:
            markers_stationary += '[' + str(coord[0]) + ',' + str(coord[1]) + '], \n'
    markers_stationary += ']\n'

    travel_full_text = ''
    markers_travel = '\nvar markers_travel = ['
    for cluster in travel_clusters:
        min_coord, max_coord = gps.getboundary(cluster)
        to_insert = 'north: ' + str(min_coord[0]) + ', \n west: '+ str(min_coord[1]) + ', \n' \
                    ' south: ' + str(max_coord[0]) + ', \n east: '+ str(max_coord[1]) + '\n }\n});'
        travel_full_text += 'var rect'+str(idx)+'=' + rectangle_t_txt + to_insert + '\n'
        idx += 1
        for coord in cluster:
            markers_travel += '[' + str(coord[0]) + ',' + str(coord[1]) + '], \n'
    markers_travel += ']\n'

    markers_full_text = 'var markers = ['
    for marker in noise_markers:
        markers_full_text += '[' + str(marker[0]) + ', ' + str(marker[1]) + '], \n'
    markers_full_text += ']' + markers_stationary + markers_travel + marker_txt

    #final_txt = start_txt + stationary_full_text + travel_full_text + markers_full_text + end_txt
    final_txt = start_txt + markers_full_text + end_txt
    f = open(path_to_use, 'w')
    f.write(final_txt)
    f.close()

