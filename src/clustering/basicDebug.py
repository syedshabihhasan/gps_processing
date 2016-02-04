def writecluster(pid, clusters, c_type = 'S'):
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
    f = open('./debug/'+pid+'_'+c_type+'.cluster', 'w')
    f.write(toWrite)
    f.close()