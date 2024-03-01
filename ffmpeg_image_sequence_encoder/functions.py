import os
import platform
import subprocess as sp
import json
import re

TOOL_NAME = "FFmpeg Image Sequence Encoder"

PREF_FILENAME = "preferences.json"


def write_pref_file(ffmpeg_path=''):

    # Prefs to save : Source Dir Path, Output Dir Path, Checkbox State
    preferences = {
        "ffmpeg_path": ffmpeg_path,
    }

    # Get the directory path where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path for the JSON file
    json_file_path = os.path.join(script_dir, PREF_FILENAME)

    # Write the preferences data to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(preferences, json_file, indent=4)

    print("Preferences saved to:", json_file_path)


def read_pref_file(preference):

    # Get the directory path where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path for the JSON file
    json_file_path = os.path.join(script_dir, PREF_FILENAME)

    user_pref = None

    if os.path.exists(json_file_path) is True:
        # Read the JSON data from the file
        file = open(json_file_path)
        preferences = json.load(file)

        user_pref = preferences[str(preference)]
        return user_pref

    return user_pref


def get_ffmpeg_path_pref():
    ffmpeg_path = os.path.normpath(read_pref_file('ffmpeg_path'))
    if os.path.isfile(ffmpeg_path) is True:
        return ffmpeg_path

    print('FFmpeg path was not found!')
    return


def open_dir(path):
    fixed_path = os.path.normpath(path)
    print('Trying to open directory path: ' + fixed_path)
    if os.path.isdir(fixed_path):
        if platform.system() == 'Windows':

            cmd = ['explorer', fixed_path]

        elif platform.system() == 'Darwin':

            cmd = ['open', '%s' % fixed_path]

        elif platform.system() == 'Linux':
            cmd = ['xdg-open', '%s' % fixed_path]
        sp.call(cmd)
    else:
        print('The following directory does not exist: ' + fixed_path)


def get_in_out_files(file_path):
    dir_path = os.path.dirname(file_path)
    full_file_name = os.path.basename(file_path)
    base_file_name, file_extension = os.path.splitext(full_file_name)

    # Extract the numeric part from the end of the file name
    numeric_part = re.search(r'\d+$', base_file_name)
    num_digits = len(numeric_part)

    # Remove the numeric part from the file name
    clean_file_name = base_file_name[:-num_digits]

    input_file_name = os.path.join(dir_path, clean_file_name)
    output_file_name = os.path.join(dir_path, clean_file_name)

    return input_file_name, output_file_name, file_extension


def encode_with_ffmpeg(input_file, output_file, file_extension, fps_value):

    input_file = os.path.normpath(input_file) + '%04d' + file_extension
    output_file = os.path.normpath(output_file) + '.mov'
    ffmpeg_path = get_ffmpeg_path_pref()
    print(ffmpeg_path)

    # THE CRF FLAG IS FOR QUALITY CONSTANT, FROM  0 TO 63
    if file_extension == '.exr':
        cmd = [
            ffmpeg_path,
            '-y',
            '-gamma', '2.2',
            '-i', input_file,
            '-r', fps_value,
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-crf', '18',
            output_file
        ]

    else:
        cmd = [
            ffmpeg_path,
            '-y',
            '-i', input_file,
            '-r', fps_value,
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-crf', '18',
            output_file
        ]

    process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)

    print('Encoding Started')

    # Wait for the process to finish and capture its output
    stdout, stderr = process.communicate()

    # Check the return code to determine if the process completed successfully
    if process.returncode == 0:
        print('Process completed successfully!')

    else:
        print('Process failed with return code:', process.returncode)
