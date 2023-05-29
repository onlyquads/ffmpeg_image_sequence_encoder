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
        file_name = os.path.basename(file_path)


        list_dir = os.listdir(dir_path)
        file_list = []
        file_count = 0
        for i in list_dir:
            print i
            file_list.append(i)
            file_count = file_count + 1



        



        
        print (file_count)
        print ('File path = ' + file_path)
        print ('Dir path =' + dir_path)




    def exists(self ):
        return cmds.window(self.window, q=True, ex=True)

    def refresh (self):
        #Refresh command
        print ('Refreshing')    

    def show(self):
        # Show the window
        cmds.showWindow(self.window)
        
ffmpeg_encoder_main_window = FFPMPEG_ENCODER_WINDOW()
ffmpeg_encoder_main_window.show()


