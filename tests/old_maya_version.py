import os
import maya.cmds as cmds
import functions


ffmpeg_path = '/opt/homebrew/Cellar/ffmpeg/6.0/bin/ffmpeg'
tool_name = 'FFmpeg Image Sequence Encoder'

    
def show_success_popup():
    result = cmds.confirmDialog(title="Encode Done !", message="Ffmpeg encode is now completed", button="OK", defaultButton="OK")
    if result == "OK":
        print("Popup closed.")

def show_failed_popup():
    result = cmds.confirmDialog(title="Encode Failed !", message="Ffmpeg encode failed", button="OK", defaultButton="OK")
    if result == "OK":
        print("Popup closed.")



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
        functions.open_dir(path)

            
    def browse_image(self, *args):
        file_path = cmds.fileDialog2(fileMode=1, caption="Select EXR Image", fileFilter="EXR Files (*.exr)")[0]

        if file_path:
            self.image_path = file_path
            cmds.textFieldButtonGrp(self.file_text_field, edit=True, text=self.image_path)


    def get_image_sequence(self, *args):

        file_path = cmds.textFieldButtonGrp(self.file_text_field, q=True, text=True)
        input_file_name, output_file_name = functions.get_in_out_files(file_path)
        # Launnch FFmpeg encode:
        functions.encode_with_ffmpeg(input_file = input_file_name, output_file=output_file_name )


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

show_main_window()
