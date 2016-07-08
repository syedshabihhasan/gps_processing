class SurveyConstants:
    '''
    0 patient,
    1 condition,
    2 session,
    3 survey,
    4 start-time,
    5 end-time,
    6 app-welcome,
    7 listening,
    8 duration,
    9 subject-bash,
    10 subject-welcome,
    11 acSpeech,
    12 ac,
    13 location,
    14 lc,
    15 tf,
    16 vc,
    17 tl,
    18 nz,
    19 nl,
    20 rs,
    21 cp,
    22 sp,
    23 le,
    24 ld,
    25 ld2,
    26 lcl,
    27 hau,
    28 hapq,
    29 st,
    30 ap,
    31 qol,
    32 im,
    33 user-initiated,
    34 gpsPath,
    35 surveyPath,
    36 audioPath
    '''
    PATIENT_ID = 0
    CONDITION_ID = 1
    SESSION_ID = 2
    SURVEY_ID = 3
    START_TIME = 4
    END_TIME = 5
    APP_WELCOME = 6
    LISTENING = 7
    EVENT_ENDED_LT_1HR = 8
    EVENT_ENDED_GT_1HR = 9
    SUBJECT_WELCOME = 10
    SPEECH = 11
    ACTIVITY_CONTEXT = 12
    LOCATION = 13
    LOCATION_CONTEXT = 14
    TALKER_FAMILIARITY = 15
    VISUAL_CUES = 16
    TALKER_LOCATION = 17
    NOISINESS = 18
    NOISE_LOCATION = 19
    ROOM_SIZE = 20
    CARPETING = 21
    SPEECH_PERCEPTION = 22
    LISTENING_EFFORT = 23
    LOUDNESS = 24
    LOUDNESS_SATISFACTION = 25
    LOCALIZATION = 26
    HEARING_AID_USE = 27
    HEARING_AID_PROGRAM = 28
    SATISFACTION = 29
    ACTIVITY_PARTICIPATION = 30
    QUALITY_OF_LIFE = 31
    IMPORTANCE = 32
    USER_INITIATED = 33
    GPS_PATH = 34
    SURVEY_PATH = 35
    AUDIO_PATH = 36

class LocationContext:
    LOCATION_CONTEXT_VALUES = {'1': 'out/traffic',
                               '2': 'out/other',
                               '3': 'in/home',
                               '4': 'in/other',
                               '5': 'in/crowd'}