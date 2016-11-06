from tqdm import tqdm
import argparse
import os
import traceback
import pickle


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '-I', help='Folder with survey, gps, and audio files', required=True)
    parser.add_argument('-g', '-G', help='include gps values', action='store_true')
    parser.add_argument('-o', '-O', help='Path of file to output the data into', required=True)
    parser.add_argument('-e', '-E', help='Folder to store error variables, with leading /', required=True)

    args = parser.parse_args()

    return args.i, args.g, args.o, args.e


def get_file_list(dir_paths, file_type):
    files = []
    for root, dirnames, filenames in os.walk(dir_paths):
        for filename in filenames:
            if filename.endswith(file_type):
                files.append(os.path.join(root, filename))
    return files


def match_files(filename, file_list):
    split_filename = filename.split('/')[-1].split('.')
    to_match = '.'.join(split_filename[:3]) + '.' + split_filename[3].split(' ')[0]
    return [x for x in file_list if to_match in x]


def read_survey_file(survey_filename):
    with open(survey_filename, 'r') as f:
        survey_data = f.read().splitlines()
    survey_dict = {x.split('=')[0]: x.split('=')[1] for x in survey_data}
    if 'survey' in survey_dict:
        survey_dict['session'] = survey_dict['survey']
    survey_dict['condition'] = survey_filename.split('/')[-1].split('.')[1]
    return survey_dict


def read_gps_file(gps_filename):
    with open(gps_filename, 'r') as f:
        gps_data = f.read()
    if gps_data == '':
        return None
    gps_data = gps_data.splitlines()
    to_return = []
    for line in gps_data:
        line = line.split(',')
        to_return.append([line[1], line[0], line[2]])
    return to_return


def compile_survey_into_text(survey_dict, survey_file, audio_file, gps_file, include_gps=False, first=False):
    tags = ['patient', 'condition', 'session', 'survey', 'start-time', 'end-time', 'app-welcome', 'listening',
            'duration', 'subject-bash', 'subject-welcome', 'acSpeech', 'ac', 'location',
            'lc', 'tf', 'vc', 'tl', 'nz', 'nl', 'rs', 'cp', 'sp', 'le', 'ld', 'ld2', 'lcl', 'hau', 'hapq',
            'st', 'ap', 'qol', 'im', 'user-initiated', 'gpsPath', 'surveyPath', 'audioPath']
    if first:
        to_ret = ','.join(tags)
        if include_gps:
            to_ret += ',gpsLat,gpsLon,gpsAcc'
        return to_ret

    tag_list = []
    for tag in tags:
        if tag == 'gpsPath':
            tag_list.append(gps_file[0] if gps_file else '')
        elif tag == 'surveyPath':
            tag_list.append(survey_file)
        elif tag == 'audioPath':
            tag_list.append(audio_file[0] if audio_file else '')
        tag_val = survey_dict[tag]
        tag_list.append(tag_val)

    survey_text = ','.join(tag_list)
    to_return = ''

    if include_gps:
        if gps_file:
            gps_data = read_gps_file(gps_file[0])
            if not gps_data:
                to_return = survey_text + ',,,'
            else:
                for gps_datum in gps_data:
                    to_return += survey_text + ',' + gps_datum[0] + ',' + gps_datum[1] + ',' + gps_datum[2] + '\n'
                to_return = to_return[:-1]
        else:
            to_return = survey_text + ',,,'

    return to_return


def write_csv(to_write, to_write_at):
    with open(to_write_at, 'w') as f:
        f.write(to_write)


def main():
    print('Parsing input arguments')
    input_folder, include_gps, output_file, error_folder = get_cli_args()
    print('Getting file lists')
    survey_file_list = get_file_list(input_folder, '.survey')
    gps_file_list = get_file_list(input_folder, '.gps')
    audio_file_list = get_file_list(input_folder, '.audio')
    print('Starting analysis\n')
    problem_files = []
    error_files = []
    to_write = ''
    header = compile_survey_into_text(None, None, None, None, include_gps, True)
    to_write += header + '\n'
    for survey_filename in tqdm(survey_file_list):
        survey_dict = read_survey_file(survey_filename)
        matching_audio = match_files(survey_filename, audio_file_list)
        matching_gps = match_files(survey_filename, gps_file_list)
        if len(matching_audio) > 1 or len(matching_gps) > 1:
            problem_files.append([survey_filename, matching_audio, matching_gps])
        try:
            text_form_survey = compile_survey_into_text(survey_dict, survey_filename, matching_audio,
                                                        matching_gps, include_gps)
        except:
            error_files.append([survey_filename, matching_audio, matching_gps, traceback.format_exc()])
            continue
        to_write += text_form_survey + '\n'
    print('\nWriting the CSV file')
    write_csv(to_write, output_file)
    print('Writing the error files')
    with open(error_folder + 'error.dat', 'wb') as f:
        pickle.dump(error_files, f)
    print('TADAA!!')


if __name__ == "__main__":
    main()
