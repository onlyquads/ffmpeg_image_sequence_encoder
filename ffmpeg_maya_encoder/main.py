import os
import platform
import re
import maya.cmds as cmds
import subprocess as sp


ffmpeg_path = '/opt/homebrew/Cellar/ffmpeg/5.1.2_3/bin/ffmpeg'
tool_name = 'FFmpeg Image Sequence Encoder'

def fix_platform_path(path):

    if path is None:
        return

    if platform.system() == "Windows":
        path = path.replace("/", "\\")
    else:
        path = path.replace("\\", "/")

    return path
    
def show_success_popup():
    result = cmds.confirmDialog(title="Encode Done !", message="Ffmpeg encode is now completed", button="OK", defaultButton="OK")
    if result == "OK":
        print("Popup closed.")

def show_failed_popup():
    result = cmds.confirmDialog(title="Encode Failed !", message="Ffmpeg encode failed", button="OK", defaultButton="OK")
    if result == "OK":
        print("Popup closed.")



def open_dir(path):
    fixed_path = fix_platform_path(path)
    print("Trying to open directory path: " + fixed_path)
    if os.path.isdir(fixed_path):
        if platform.system()=="Windows":
        
            cmd = ["explorer", fixed_path]

        elif platform.system()=="Darwin":

            cmd = ["open", "%s" % fixed_path]

        elif platform.system()=="Linux":
            cmd = ["xdg-open", "%s" % fixed_path]

        sp.call(cmd)
    else:
        cmds.warning("The following directory doesn't exist: " + fixed_path)


def encode_with_ffmpeg(input_file, output_file):


    input_file = fix_platform_path(input_file) +"%04d.exr" 
    output_file = fix_platform_path(output_file) + '.mov'

    cmd = [
        ffmpeg_path,
        '-y',
        '-gamma', '2.2',
        '-i', input_file,
        '-r', '25',
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
        print("Process completed successfully!")
        show_success_popup()

    else:
        print("Process failed with return code:", process.returncode)
        show_failed_popup()



class FFPMPEG_ENCODER_WINDOW(object):
 
    def __init__(self):

        # Window Layout setup
        
        self.window = cmds.window(title = tool_name) 
        self.column = cmds.columnLayout(adj=True)
        cmds.text(tool_name)
        cmds.separator(h=5)
       
        self.file_text_field = cmds.textFieldButtonGrp(label="Image Path: ", buttonLabel="Browse", buttonCommand=self.browse_image)
       
        cmds.separator(h=5)
        encode_button = cmds.button(l='Encode!', command = self.get_image_sequence)
        reveal_folder = cmds.button(l='Reveal in Explorer', command= self.reveal_folder)
        self.contents = []
        self.refresh ()


    def reveal_folder(self, *args):
        file_path =cmds.textFieldButtonGrp(self.file_text_field, q=True, text=True)
        
        path = os.path.dirname(file_path)
        open_dir(path)

            
    def browse_image(self, *args):
        file_path = cmds.fileDialog2(fileMode=1, caption="Select EXR Image", fileFilter="EXR Files (*.exr)")[0]

        if file_path:
            self.image_path = file_path
            cmds.textFieldButtonGrp(self.file_text_field, edit=True, text=self.image_path)


    def get_image_sequence(self, *args):

        file_path = cmds.textFieldButtonGrp(self.file_text_field, q=True, text=True)
        dir_path = os.path.dirname(file_path)
        full_file_name = os.path.basename(file_path)
        split_extension = full_file_name.split('.exr')
        file_name = split_extension[0]
        clean_file_name = file_name[0:-4]
        input_dir = dir_path + '/' + clean_file_name
        movie_file_name = clean_file_name
        output_dir = dir_path + '/' + movie_file_name


        # Let's list the given directory and count how many frames we have
        list_dir = os.listdir(dir_path)
        file_list = []
        frame_count = 0
        for i in list_dir:
            print i
            file_list.append(i)
            frame_count = frame_count + 1

        # Launnch FFmpeg encode:

        encode_with_ffmpeg(input_file = input_dir, output_file=output_dir )

        


    def exists(self ):
        return cmds.window(self.window, q=True, ex=True)

    def refresh (self):
        #Refresh command
        print ('Refreshing')    

    def show(self):
        # Show the window
        cmds.showWindow(self.window)


def show_main_window():
    ffmpeg_encoder_main_window = FFPMPEG_ENCODER_WINDOW()
    ffmpeg_encoder_main_window.show()


