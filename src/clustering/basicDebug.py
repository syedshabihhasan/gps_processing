import os
import pickle


def writecluster(pid, clusters, op_path, c_type='S', cluster_label=None):
    toWrite = ''
    if 'S' is c_type or 'T' is c_type:
        for c_idx in range(len(clusters)):
            cluster = clusters[c_idx]
            toWrite += '\n'
            for coord in cluster:
                for idx in range(len(coord)):
                    toWrite += str(coord[idx]) + ' '
                if cluster_label is not None:
                    toWrite += cluster_label[c_idx] + ' '
                toWrite += '\n'
    elif 'N' is c_type:
        for coord in clusters:
            for idx in range(len(coord)):
                toWrite += str(coord[idx]) + ' '
            toWrite += '\n'
    final_path = op_path + '/debug/'
    if not os.path.exists(final_path):
        os.makedirs(final_path)
    f = open(final_path + pid + '_' + c_type + '.cluster', 'w')
    f.write(toWrite)
    f.close()


def write_variable(variable, filename, op_path):
    final_path = op_path + '/debug/'
    if not os.path.exists(final_path):
        os.makedirs(final_path)
    with open(op_path + '/debug/' + filename, 'wb') as f:
        pickle.dump(variable, f)
