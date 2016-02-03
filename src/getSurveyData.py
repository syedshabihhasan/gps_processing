__author__ = 'hasanshabih'
import os;
import fnmatch;
import sys;

def getCorrespondingFile(filename, listDB):
    f_split = filename.split('/')[-1];	# get the actual file name
    # #print f_split;
    match = f_split.split('.')[0]+'.'+f_split.split('.')[1]+'.'+f_split.split('.')[2]+'.'+f_split.split('.')[3].split(' ')[0];
    return [x for x in listDB if match in x];

def getFilenames(dirPaths,fileType):
    files = [];
    for root,dirnames,filenames in os.walk(dirPaths):
        for filename in fnmatch.filter(filenames,'*.'+fileType):
            files.append(os.path.join(root,filename));
    return files;

def initVars():
    tags = ['patient','condition','session','survey','start-time','end-time','app-welcome',\
            'listening','duration','subject-bash','subject-welcome','acSpeech','ac','location',\
            'lc','tf','vc','tl','nz','nl','rs','cp','sp','le','ld','ld2','lcl','hau','hapq','st',\
            'ap','qol','im','user-initiated','gpsPath', 'surveyPath','audioPath'];
    tagVals = {};
    for tag in tags:
        tagVals[tag] = ' ';
    return tags,tagVals;

def writeCSV(bigText,filename):
    f = open(filename,'a');
    f.write(bigText);
    f.close();
    return f.closed;

def main():
    bigText = '';
    tags,tagVals = initVars();
    for i in range(len(tags)-1):
        bigText+=tags[i]+',';
    bigText+=tags[-1]+'\r';
    #get all the survey file names, fill up the dictionary, get the corresponding gps file name (get all in a list)
    # #put all in a bigText variable, write
    surveyFiles = [];
    gpsFiles = [];
    audioFiles = [];
    for i in range(1,len(sys.argv)-1):
        surveyFiles += getFilenames(sys.argv[i],'survey');
        gpsFiles += getFilenames(sys.argv[i],'gps');
        audioFiles += getFilenames(sys.argv[i],'audio');
    for surveyFile in surveyFiles:
        tags,tagVals = initVars();
        f = open(surveyFile,'r');
        surveyValPresent = False;
        t = f.read();
        f.close();
        if '' == t:
            continue;
        t = t.split('\r');
        try:
            t.remove('');
        except ValueError:
            print 'Value error, survey file, ', surveyFile;
        for tV in t:
            tV = tV.split('=');
            tagVals[tV[0]] = tV[1];
            if tV[0] == 'survey':
                surveyValPresent = True;
        if surveyValPresent:
            tagVals['session'] = tagVals['survey'];
            surveyValPresent = False
        corrGPS = getCorrespondingFile(surveyFile,gpsFiles);
        if 1 == len(corrGPS):
            tagVals['gpsPath'] = corrGPS[0];
        else:
            tagVals['gpsPath'] = ''
            print 'len(corrGPS) != 1, survey file (', surveyFile, '), gps files(', corrGPS, ')'
        cond = surveyFile.split('/')[-1].split('.')[1];
        tagVals['condition'] = cond;
        tagVals['surveyPath'] = surveyFile;
        corrAudio = getCorrespondingFile(surveyFile, audioFiles);
        if 1 == len(corrAudio):
            tagVals['audioPath'] = corrAudio[0];
        else:
            print ' len(corrAudio)!=1 survey file (',surveyFile,'), audio files(',corrAudio,'), skipping';
            continue;
        for i in range(len(tags)-1):
            bigText+= tagVals[tags[i]]+',';
        bigText+=tagVals[tags[-1]]+'\r';
    writeCSV(bigText,sys.argv[-1]);

if __name__ == "__main__":
    if 1 == len(sys.argv):
        print "Usage: python getSurveyData.py <paths to survey files> ... <path to file where output is to be saved>";
    else:
	    main();