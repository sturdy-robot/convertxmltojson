import os
import logging
import xmltodict
import json
from xml.parsers.expat import ExpatError


def get_files(path_to_file):
    logging.debug('Getting files')
    files = []
    path_to_file = os.path.normpath(path_to_file)

    for path, _, files_dir in os.walk(path_to_file):
        for file in files_dir:
            if file.endswith(".xml"):
                filepath = os.path.join(path, file)
                logging.debug('Got file: ' + filepath)
                files.append(filepath)
    
    return files


def read_xml(filepath):
    logging.debug('Reading XML file ' + filepath)
    with open(filepath, 'r', encoding='utf-8') as fp:
        return fp.read()


def convert_xml(data):
    logging.debug('Converting XML file')
    return xmltodict.parse(data)


def write_to_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, indent=4)


def get_json_file_names(files, output_folder):
    logging.debug('Getting json filenames')
    output_file_paths = []
    for file in files:
        file = file.split(os.path.sep)
        output_file_name = file[-1].split('.')[0] + '.json'
        output_folder_path = os.path.join(output_folder, file[-2])
        if not os.path.exists(output_folder_path):
            os.mkdir(output_folder_path)
        output_filepath = os.path.join(output_folder_path, output_file_name)
        logging.debug('Json filename: ' + output_filepath)
        output_file_paths.append(output_filepath)
    
    return output_file_paths


def run(input_folder, output_folder):
    logging.debug('Running the program')
    files = get_files(input_folder)
    output_files = get_json_file_names(files, output_folder)

    for file, output_file in zip(files, output_files):
        try:
            json_data = convert_xml(read_xml(file))
            write_to_json(json_data, output_file)
        except ExpatError:
            pass


def main():
    input_path = r'/home/sturdyrobot/bygfoot'
    output_path = r'/home/sturdyrobot/outputfolder'

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    logging.basicConfig(
        filename='convert_xml_to_json.log',
        encoding='utf-8',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
    )

    run(input_path, output_path)


if __name__ == '__main__':
    main()
