import os

def writecluster(pid, clusters, op_path, c_type = 'S'):
    toWrite = ''
    if 'S' is c_type or 'T' is c_type:
        for cluster in clusters:
            toWrite += '\n'
            for coord in cluster:
                for idx in range(len(coord)):
                    toWrite += str(coord[idx]) + ' '
                toWrite += '\n'
    elif 'N' is c_type:
        for coord in clusters:
            for idx in range(len(coord)):
                toWrite+= str(coord[idx]) + ' '
            toWrite += '\n'
    final_path = op_path + '/debug/'
    if not os.path.exists(final_path):
        os.makedirs(final_path)
    f = open(final_path+pid+'_'+c_type+'.cluster', 'w')
    f.write(toWrite)
    f.close()