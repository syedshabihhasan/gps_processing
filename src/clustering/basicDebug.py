def writecluster(pid, clusters, c_type = 'S'):
    toWrite = ''
    for cluster in clusters:
        toWrite += '\n'
        for coord in cluster:
            toWrite += ''+str(coord[0]) + ',' + str(coord[1]) + '\n'
    f = open('./debug/'+pid+'_'+c_type+'.cluster', 'w')
    f.write(toWrite)
    f.close()