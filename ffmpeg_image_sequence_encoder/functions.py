import os
import platform
import subprocess as sp

tool_name = 'FFmpeg Image Sequence Encoder'

def get_ffmpeg_path():

    # MAKE SURE FFMPEG PATH IS SETUP CORRECTLY FOR YOUR PLATFORM HERE:

    # WINDOWS
    if platform.system() == 'Windows':
        ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg'
        return ffmpeg_path
    # MAC OS
    if platform.system() == 'Darwin':
        ffmpeg_path = '/opt/homebrew/Cellar/ffmpeg/6.0/bin/ffmpeg'
        return ffmpeg_path
    # LINUX
    if platform.system() == 'Linux':
        ffmpeg_path = '/usr/local/bin/ffmpeg'
        return ffmpeg_path


def fix_platform_path(path):

    if path is None:
        return
    if platform.system() == 'Windows':
        path = path.replace('/', '\\')
    else:
        path = path.replace('\\', '/')

    return path


def open_dir(path):
    fixed_path = fix_platform_path(path)
    print('Trying to open directory path: ' + fixed_path)
    if os.path.isdir(fixed_path):
        if platform.system()=='Windows':
        
            cmd = ['explorer', fixed_path]

        elif platform.system()=='Darwin':

            cmd = ['open', '%s' % fixed_path]

        elif platform.system()=='Linux':
            cmd = ['xdg-open', '%s' % fixed_path]
        sp.call(cmd)
    else:
        print('The following directory does not exist: ' + fixed_path)


def get_in_out_files(file_path):
    dir_path = os.path.dirname(file_path)
    full_file_name = os.path.basename(file_path)
    base_file_name, file_extension  = os.path.splitext(full_file_name)
    file_name = base_file_name
    clean_file_name = file_name[0:-4]
    input_file_name = dir_path + '/' + clean_file_name
    movie_file_name = clean_file_name
    output_file_name = dir_path + '/' + movie_file_name

    return input_file_name, output_file_name, file_extension



def encode_with_ffmpeg(input_file, output_file, file_extension, fps_value):

    input_file = fix_platform_path(input_file) +'%04d'+file_extension
    output_file = fix_platform_path(output_file) + '.mov'
    ffmpeg_path = fix_platform_path(get_ffmpeg_path())

    ### THE CRF FLAG IS FOR QUALITY CONSTANT QUALITY, FROM  0 TO 63
    if file_extension == '.exr':    
        cmd = [
            ffmpeg_path,
            '-y',
            '-gamma', '2.2',
            '-i', input_file,
            '-r', fps_value,
            '-vcodec','libx264',
            '-pix_fmt','yuv420p',
            '-crf', '18',
            output_file
        ]

    else: 
        cmd = [
            ffmpeg_path,
            '-y',
            '-i', input_file,
            '-r', fps_value,
            '-vcodec','libx264',
            '-pix_fmt','yuv420p',
            '-crf', '18',
            output_file
        ]
    
    process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    
    print ('Encoding Started')
    
    # Wait for the process to finish and capture its output
    stdout, stderr = process.communicate()

    # Check the return code to determine if the process completed successfully
    if process.returncode == 0:
        print('Process completed successfully!')
        
    else:
        print('Process failed with return code:', process.returncode)

