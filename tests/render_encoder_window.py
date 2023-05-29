import os
import platform
import maya.cmds as cmds
import subprocess as sp
from PrismInit import pcore

class myWindow(object):
 
    def __init__(self):
        self.window = cmds.window(title = 'Encode Renders') 
        self.column = cmds.columnLayout( adjustableColumn=True )
        #TITLE
        cmds.separator(h=10)
        cmds.text("EXR seq. to ffmpeg")
        cmds.separator(h=10)

        #ASSET DROPDOWN
        self.asset_dropdown_menu = cmds.optionMenu( label='Asset',changeCommand=self.selected_asset, acc =True)
        asset_list = get_existing_assets()
        for i in asset_list:
           self.asset_dropdown_item = cmds.menuItem(p=self.asset_dropdown_menu, label = str(i) )
         
        cmds.separator(h=10)
        
        #VERSION DROPDOWN
        self.version_dropdown_menu = cmds.optionMenu(label='Versions', changeCommand=self.selected_version)
        version_list = get_existing_versions(asset_list[0])
        for i in version_list:
            self.version_dropdown_item = cmds.menuItem(p=self.version_dropdown_menu, label = i)

        latest_version = version_list[-1]
        cmds.optionMenu(self.version_dropdown_menu, e=True, value = latest_version)


        cmds.separator(h=10)
        
        #ENCODE BUTTON
        send_to_ffmpeg_btn = cmds.button(label="send to ffmpeg", command=self.set_exr_path)

        #OPEN RENDER FOLDER
        open_render_folder = cmds.button(label="open Render Folder", command = self.btn_open_directory)
        
        self.refresh()

    def clearList(self, *args):
        #Clear version menuItem, otherwise version menuItem keeps growing and adding more and more infos
        menuItems = cmds.optionMenu(self.version_dropdown_menu, q=True, itemListLong=True) # itemListLong returns the children
        if menuItems:
            cmds.deleteUI(menuItems)   

    def selected_asset(self, item):
        if item == '(Select Asset)':
            return
        asset_name = item
        print item
        self.clearList()
        version_list = []
        version_list = get_existing_versions(asset_name)
        
        for i in version_list:
            self.version_dropdown_item = cmds.menuItem(p=self.version_dropdown_menu, label = i)

        latest_version = version_list[-1]
        cmds.optionMenu(self.version_dropdown_menu, e=True, value = latest_version )
        self.refresh()
        return asset_name
    

    def selected_version(self, item):
        print('selected version is ' + item)

        selected_version = item
        return selected_version


    def set_exr_path(self, *arg):
        
        
        selected_asset = cmds.optionMenu(self.asset_dropdown_menu, q=True, value=True)
        selected_version = cmds.optionMenu(self.version_dropdown_menu, q=True, value=True)

        #project_path = cmds.workspace(q=True, rd=True)
        project_path = '/Volumes/Pro/0020_IMPS/001_SmurfRigs'
        asset_directory= '/03_Workflow/Assets/CHARACTERS/'
        asset_render_directory = '/Rendering/3dRender/'
        asset_render_sub_directory_list = cmds.getFileList(folder = project_path + asset_directory + selected_asset + asset_render_directory +selected_version + '/')
        
        if '.DS_Store' in asset_render_sub_directory_list:    
            asset_render_sub_directory_list.remove('.DS_Store')
        
        asset_render_sub_directory = asset_render_sub_directory_list[0]
        exr_seq_directory_path = project_path + asset_directory + selected_asset + asset_render_directory +selected_version +'/' + asset_render_sub_directory + '/'
        output_video_file_directory_path = project_path + asset_directory + selected_asset + asset_render_directory +selected_version +'/'
        print ('selected asset is ') + selected_asset
        print ('selected render version is ') + selected_version
        print ('Render folder lookup path is ') + exr_seq_directory_path

        render_file_list = cmds.getFileList(folder = exr_seq_directory_path)
        render_file_fullname = render_file_list[0]
        render_file_basename =render_file_fullname.split("__")
        render_filename = render_file_basename[0]


        input_file = exr_seq_directory_path + render_filename +"__" +"%04d.exr"
        output_file = output_video_file_directory_path + render_filename +".mov"
        
        ffmpeg_path = '/opt/homebrew/Cellar/ffmpeg/5.1.2_3/bin/ffmpeg'
        srcFile = input_file
        outFile = output_file

        print ('Input file path :' + input_file)

        print srcFile
        print outFile
        cmd = [
            ffmpeg_path,
            '-y',
            '-gamma', '2.2',
            '-i', srcFile,
            '-r', '25',
            '-vcodec','libx264',
            '-pix_fmt','yuv420p',
            '-crf', '18',
            outFile
        ]
        print cmd
        sp.Popen(cmd)

        print("encoding Started")

        
    def btn_open_directory(self, *arg):
        selected_asset = cmds.optionMenu(self.asset_dropdown_menu, q=True, value=True)
        selected_version = cmds.optionMenu(self.version_dropdown_menu, q=True, value=True)
        path = detect_render_files(selected_asset, selected_version)
        open_dir(path)


    def add_asset_items(self):
        print("add_asset")

    def exists(self):
        return cmds.window(self.window, q=True, ex=True)

    def refresh (self):
        return

    def show(self):
        cmds.showWindow(self.window)



def get_existing_assets():
    ###Check all the existing assets in PrismPipeline hierarchy
    project_root_directory_path = cmds.workspace(q=True, rd=True)
    asset_char_root_directory_path = project_root_directory_path + '03_Workflow/Assets/CHARACTERS'
    print asset_char_root_directory_path
    asset_char_list = cmds.getFileList(folder = asset_char_root_directory_path)

    asset_char_list.remove('.DS_Store')
    asset_list = []
    for i in asset_char_list :
        asset_list.append(i)
    asset_list.sort()
    return asset_list

def get_existing_versions(asset_name):
    version_list = []
    project_root_directory_path = cmds.workspace(q=True, rd=True)
    asset_render_root_directory_path = project_root_directory_path + '03_Workflow/Assets/CHARACTERS/'+asset_name+'/Rendering/3dRender/'
    version_list = cmds.getFileList(folder = asset_render_root_directory_path)
    if '.DS_Store' in version_list:
        version_list.remove('.DS_Store')
    version_list.sort()
        
    return version_list




encode_by_name_UI = myWindow()
encode_by_name_UI.show()





        
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



def detect_render_files(selected_asset, selected_version):

    #If project synced locally, the renders are not sync.
    #So we need to look for them on the network instead of local project folder
    #If the render folder is empty, let's try to find the network one

    project_name = pcore.projectName
    macos_network_project_path = '/Volumes/Pro/0020_IMPS/'
    win_network_project_path = 'X:/0020_IMPS/'



    root_project_path = cmds.workspace(q=True, rd = True)
    print ('Root project folder = ' + root_project_path)
    split_root_project_path = root_project_path.split("/")
    print (split_root_project_path)
    for i in split_root_project_path:
        if i == '' :
            split_root_project_path.remove('')
    parent_root_project_directory_name = split_root_project_path[-1]
    print ('parent project folder = ' + parent_root_project_directory_name)

    asset_directory = '/03_Workflow/Assets/CHARACTERS/'
    asset_render_directory = '/Rendering/3dRender/'

    
    asset_render_sub_directory_list = cmds.getFileList(folder = root_project_path + asset_directory + selected_asset + asset_render_directory +selected_version + '/')

    if '.DS_Store' in asset_render_sub_directory_list:    
        asset_render_sub_directory_list.remove('.DS_Store')

    asset_render_sub_directory = asset_render_sub_directory_list[0]
    print asset_render_sub_directory
    latest_render_version_directory_path = root_project_path + asset_directory + selected_asset + asset_render_directory +selected_version +'/' + asset_render_sub_directory + '/'

    render_list = cmds.getFileList(f = latest_render_version_directory_path)
    #if '.DS_Store' in render_list:
    #    render_list.remove('.DS_Store')

    if not render_list:
        print ('No Render Found, trying on Axiom Server...')
        path = macos_network_project_path + parent_root_project_directory_name + asset_directory + selected_asset + asset_render_directory +selected_version +'/'
        print ('Network path is ' + path)

        return path


    print("Searching locally")
    path = root_project_path + asset_directory + selected_asset + asset_render_directory +selected_version  +  '/'
    return path

