import os
import platform
import subprocess as sp
import json
import datetime

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


def open_dir(path):
    fixed_path = os.path.normpath(path)
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

    input_file = os.path.normpath(input_file) +'%04d'+file_extension
    output_file = os.path.normpath(output_file) + '.mov'
    ffmpeg_path = os.path.normpath(get_ffmpeg_path())

    ### THE CRF FLAG IS FOR QUALITY CONSTANT, FROM  0 TO 63
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
    
    print (cmd)
    process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    
    print ('Encoding Started')
    
    # Wait for the process to finish and capture its output
    stdout, stderr = process.communicate()

    # Check the return code to determine if the process completed successfully
    if process.returncode == 0:
        print('Process completed successfully!')
        
    else:
        print('Process failed with return code:', process.returncode)



def drawtext(
        text, x, y, color=None, font_path=None, size=36, start=None, end=None):
    if text == '{framerange}':
        print(9, color)
        return draw_framerange(x, y, color, font_path, size, start, end)
    color = color or 'white'
    text = text.replace(':', r'\:')
    text = text.replace('{frame}', '%{frame_num}')
    timetag = datetime.datetime.now().strftime(r'%Y/%m/%d %H\:%M')
    text = text.replace('{datetime}', timetag)
    args = [
        None if font_path is None else "fontfile='%s'" % font_path,
        "text='%s'" % text,
        "x=%s" % x,
        "y=%s" % y,
        "start_number=%i" % start,
        "fontcolor=%s" % color,
        "fontsize=%i" % size,
    ]
    args = ':'.join([a for a in args if a])
    return "drawtext=%s" % args

def draw_framerange(
        x, y, color, font_path=None, size=36, start=None, end=None):
    # framerange is made of two separate texts:
    left_text, right_text = '{frame}', '[%i-%i]' % (start, end)
    x = str(x)
    if '/2' in x:
        # middle
        left_x = '%s-(tw/2)-3' % x
        right_x = '%s+(tw/2)+3' % x
    elif 'w-' in x.replace('tw-', ''):
        # right
        x = x.replace('tw', 'tw/2')
        # ffmpeg doesnt allow to align text on another text. Offset
        # position by a fixed amount:
        left_x = '%s-%i-(tw/2)-3' % (x, size * 6)
        right_x = '%s-%i+(tw/2)+3' % (x, size * 6)
    else:
        # left
        left_x = '%s+%i-(tw)-3' % (x, size * 3)
        right_x = '%s+%i+3' % (x, size * 3)
    return ','.join((
        drawtext(left_text, left_x, y, color, font_path, size, start),
        drawtext(right_text, right_x, y, color, font_path, size, start)
    ))


def get_padding_values(width, height, target_width, target_height):
    scale_x = float(target_width) / width
    scale_y = float(target_height) / height
    scale = min(scale_x, scale_y)
    if scale_x <= scale_y:
        image_width = target_width
        image_height = round(height * scale)
        x_offset = 0
        y_offset = round((target_height - image_height) / 2)
    else:
        # black bars on the side instead of top/bottom:
        image_width = round(width * scale)
        x_offset = round((target_width - image_width) / 2)
        y_offset = 0
    return image_width, x_offset, y_offset




def imagepos(x, y):
    return '[0:v][1:v]overlay=%i:%i' % (x, y)


def drawbox(x, y, width, height, color, opacity, thickness):
    return 'drawbox=x=%s:y=%s:w=%s:h=%s:color=%s@%s:t=%s' % (
        x, y, width, height, color, opacity, thickness)




def encode_with_ffmpeg_overlays(input_file, output_file, file_extension, fps_value, project_name = None, artist_name = None, shot_name = None, rectangles = None, logo_path = None):

    input_file = os.path.normpath(input_file) +'%04d'+file_extension
    output_file = os.path.normpath(output_file) + '.mov'
    ffmpeg_path = os.path.normpath(get_ffmpeg_path())
    
    rectangle1 = dict(x=96, y=60, width=768, height=480, color='#FFEE55', opacity=.2, thickness=2)
    rectangle2 = dict(x=144, y=90, width=672, height=420, color='#909090', opacity=.3, thickness=1)

    rectangles =  [rectangle1, rectangle2]
    frame_rate = fps_value
    frame_rate = frame_rate or 24
    start = 1
    start = start or 0
    end = 100
    end = end or 100

    source_width = 1920
    source_height = 1080


    top_left = "top left text"
    top_middle = "top middle text"
    top_right = "top right text"
    bottom_left = "bottom left text"
    bottom_middle = "bottom middle text"
    bottom_right = "bottom right text"
    text_color = "#000000"
    top_left_color = text_color
    top_middle_color = text_color
    top_right_color = text_color
    bottom_left_color = text_color
    bottom_middle_color = text_color
    bottom_right_color = text_color


    font_scale = 1

    filter_complex = []

    font_path = '/Users/hades/SynologyDrive/DEV/Git-Repo/ffmpeg_image_sequence_encoder/ffmpeg_image_sequence_encoder/font/open-sans/OpenSans-Regular.ttf'

    font_path = os.path.normpath(font_path)
    print('Font path?')
    print(os.path.exists(font_path))

    
    
    if source_width and source_height:
        width, height = source_width, source_height
    
    target_width = source_width
    target_height = source_height

    target_width = target_width or width
    target_height = target_height or height
    # Scaling and padding
    image_width, x_offset, y_offset = get_padding_values(
        width, height, target_width, target_height)
    filter_complex.append('scale=%i:-1' % image_width)
    filter_complex.append('pad=%i:%i:%i:%i' % (
        target_width, target_height, x_offset, y_offset))

    # Overlay text
    font_size = round(target_width / 53.0 * font_scale)
    margin_size = left_pos = top_pos = round(target_width / 240.0)
    right_pos = 'w-%i-(tw)' % margin_size
    bottom_pos = target_height - font_size - margin_size
    middle_pos = '(w-tw)/2'
    kwargs = dict(font_path=font_path, size=font_size, start=start, end=end)
    filters_args = (
        (top_left, left_pos, top_pos, top_left_color),
        (top_middle, middle_pos, top_pos, top_middle_color),
        (top_right, right_pos, top_pos, top_right_color),
        (bottom_left, top_pos, bottom_pos, bottom_left_color),
        (bottom_middle, middle_pos, bottom_pos, bottom_middle_color),
        (bottom_right, right_pos, bottom_pos, bottom_right_color))

    for text, left, top, color in filters_args:
        if not text:
            continue
        filter_complex.append(drawtext(text, left, top, color, **kwargs))



    if logo_path:
        filter_complex.append(imagepos(logo_path['x'], logo_path['y']))
        print('image found')

    # Add boxes (rectangles/safe-frames)
    for rectangle in rectangles or []:
        filter_complex.append(drawbox(**rectangle))


    ### THE CRF FLAG IS FOR QUALITY CONSTANT, FROM  0 TO 63
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
        # Format filter complex
        cmd += ' -filter_complex "%s"' % ','.join(filter_complex)


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

        # Format filter complex
        cmd += ' -filter_complex "%s"' % ','.join(filter_complex)

    
    print (cmd)
    process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    
    print ('Encoding Started')
    
    # Wait for the process to finish and capture its output
    stdout, stderr = process.communicate()

    # Check the return code to determine if the process completed successfully
    if process.returncode == 0:
        print('Process completed successfully!')
        
    else:
        print('Process failed with return code:', process.returncode)




def update_preference(name, value):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "preferences.json")

    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            preferences = json.load(file)
    else:
        preferences = {}

    preferences[name] = value

    with open(filename, 'w') as file:
        json.dump(preferences, file)

    print("Preference '{}' updated and saved to {}.".format(name, filename))


def read_preference(name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "preferences.json")

    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            preferences = json.load(file)
            if name in preferences:
                return preferences[name]
            else:
                print("Preference '{}' does not exist.".format(name))
                return None
    else:
        print("Preferences file does not exist.")
        return None


def read_pref_file(pref):

    # Get the directory path where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path for the JSON file
    json_file_path = os.path.join(script_dir, "preferences.json")
    
    user_pref = None

    if os.path.exists(json_file_path) == True:
        # Read the JSON data from the file
        f = open(json_file_path)
        preferences = json.load(f)

        user_pref = preferences[str(pref)]
        return user_pref
    
    return user_pref
