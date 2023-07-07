
import os 
import sys
from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QLabel, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QFrame, QSpinBox, QCheckBox
import functions

### FOR MAC OS WE NEED THIS LINE FOR PYTHON 2.7
os.environ['QT_MAC_WANTS_LAYER'] = '1'


class Encoding_Window(QMainWindow):
    def __init__(self):
        super(Encoding_Window, self).__init__()
        self.setWindowTitle(functions.tool_name)
        
        
        self.load_main_ui()
        self.load_user_inputs()

        self.check_prefs()


    def load_main_ui(self):    

        
        # Create a central widget and layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create a text field for the file path
        self.filepath_field = QLineEdit()
        self.filepath_field.textChanged.connect(self.handle_filepath_changed)
        self.main_layout.addWidget(self.filepath_field)

        
        # Create a browse button
        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.browse_files_restricted)
        self.main_layout.addWidget(browse_button)

        # Create a separator
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.HLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(separator_line)

        # Create a horizontal layout for Label and FPS spinBox
        fps_layout = QHBoxLayout()

        # Create a label for the FPS spinBox
        fps_label = QLabel('Set FPS')
        fps_layout.addWidget(fps_label)

        # Create a spinbox to set FPS
        self.fps_spinbox = QSpinBox()
        self.fps_spinbox.setMinimum(1)
        self.fps_spinbox.setValue(24)
        fps_layout.addWidget(self.fps_spinbox)
        self.main_layout.addLayout(fps_layout)

        # Create the encode button
        encode_button = QPushButton('Encode')
        encode_button.clicked.connect(self.encode_with_ffmpeg)
        self.main_layout.addWidget(encode_button)

        # Create the open directory button
        open_dir_button = QPushButton('Open Directory')
        open_dir_button.clicked.connect(self.open_dir)
        self.main_layout.addWidget(open_dir_button)

        self.setCentralWidget(self.central_widget)
        

    def load_user_inputs(self):

        # User Inputs Layout
        self.user_input_main_layout = QVBoxLayout()

        # Project Name Layout
        self.project_name_layout = QHBoxLayout()

        # Set project name
        self.project_name_label = QLabel('Project Name :')
        self.project_name_line_edit = QLineEdit()
        self.project_name_line_edit.textChanged.connect(self.handle_project_name_changed)

        self.project_name_layout.addWidget(self.project_name_label)
        self.project_name_layout.addWidget(self.project_name_line_edit)

        # Add to  main layout
        self.user_input_main_layout.addLayout(self.project_name_layout)
        
        # Set artist name layout
        self.artist_name_layout = QHBoxLayout()

        # Set artist name
        self.artist_name_label = QLabel('Artist Name :')
        self.artist_name_line_edit = QLineEdit()
        self.artist_name_line_edit.textChanged.connect(self.handle_artist_name_changed)

        self.artist_name_layout.addWidget(self.artist_name_label)
        self.artist_name_layout.addWidget(self.artist_name_line_edit)
        
        # Add to  main layout
        self.user_input_main_layout.addLayout(self.artist_name_layout)

        # Set shot name layout
        self.shot_name_layout = QHBoxLayout()

        # Set shot name
        self.shot_name_label = QLabel('Shot Name :')
        self.shot_name_line_edit = QLineEdit()
        self.shot_name_line_edit.textChanged.connect(self.handle_shot_name_changed)

        self.shot_name_layout.addWidget(self.shot_name_label)
        self.shot_name_layout.addWidget(self.shot_name_line_edit)
        
        # Add to  main layout
        self.user_input_main_layout.addLayout(self.shot_name_layout)
        
        # Logo layout
        self.logo_setup_main_layout = QVBoxLayout()
        self.logo_setup_layout = QHBoxLayout()

        # Set Logo
        self.enable_logo_checkbox = QCheckBox('Enable Logo')

        self.set_logo_file_button = QPushButton('Browse')
        self.set_logo_file_button.clicked.connect(self.handle_set_logo_file_button_pressed)
        self.set_logo_file_line_edit = QLineEdit('Set up logo')
        self.set_logo_file_line_edit.textChanged.connect(self.handle_logo_path_changed)

        self.logo_setup_layout.addWidget(self.set_logo_file_button)
        self.logo_setup_layout.addWidget(self.set_logo_file_line_edit)

        self.logo_setup_main_layout.addWidget(self.enable_logo_checkbox)
        self.logo_setup_main_layout.addLayout(self.logo_setup_layout)

        # Add to  main layout
        self.user_input_main_layout.addLayout(self.logo_setup_main_layout)



        separator = self.create_separator()
        self.user_input_main_layout.addWidget(separator)

        # Add to main layout
        self.main_layout.addLayout(self.user_input_main_layout)



    def load_advanced_ui(self):
        print('Loading advanced UI Panel')



    def handle_project_name_changed(self):
        print('Project name changed')
        self.update()

    def handle_artist_name_changed(self):
        print('Artist name changed')
        self.update()

    def handle_shot_name_changed(self):
        print('Shot name changed')
        self.update()


    def handle_set_logo_file_button_pressed(self):
        print('Browse for logo button pressed')
        selected_logo = self.browse_files()
        self.set_logo_file_line_edit.setText(selected_logo)
        #self.update()

    def handle_logo_path_changed(self):
        print('Logo path changed')
        logo_path_name = 'logo_file_path'
        logo_path = self.set_logo_file_line_edit.text()
        functions.update_preference(name = logo_path_name,value = logo_path)

    
    def handle_filepath_changed(self):
        source_path_name = 'source_file_path'
        source_path = self.filepath_field.text()
        functions.update_preference(name = source_path_name  , value = source_path)

    def browse_files_restricted(self):
        # Open the file browser and filter for supported image files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('EXR Sequence (*.exr *.jpg *.jpeg *.tiff *.png)')
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.filepath_field.setText(selected_files[0])

    def browse_files(self):
        # Open the file browser and filter for supported image files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('(*.exr *.jpg *.jpeg *.tiff *.png)')
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()[0]
            return selected_files

    def browse_folder(self):
        # Open the file browser and restrict to select a only a folder
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        
        if file_dialog.exec_():
            selected_folder = file_dialog.selectedFiles()[0]
            return selected_folder



    
    def encode_with_ffmpeg(self):
        # Get specified FPS
        fps_value = self.fps_spinbox.text()
        # Get the file path
        file_path = self.filepath_field.text()
        # Get the input name formated with %04d and the output file
        input_file_name, output_file_name, file_extension = functions.get_in_out_files(file_path)
        # Start the encoding process
        functions.encode_with_ffmpeg_overlays(input_file_name, output_file_name, file_extension, fps_value)
    
    def open_dir(self):
        file_path = self.filepath_field.text()
        path = os.path.dirname(file_path)
        functions.open_dir(path)


    def check_prefs(self):
        source_file_path = functions.read_preference('source_file_path')
        output_dir_path = functions.read_preference('output_dir_path')
        logo_file_path = functions.read_preference('logo_file_path')
        checkbox_state = functions.read_preference('checkbox_state')
        project_name = functions.read_preference('project_name')
        artist_name = functions.read_preference('artist_name')
        shot_name = functions.read_preference('shot_name')

        if source_file_path != None:
            self.filepath_field.setText(source_file_path)
        if output_dir_path != None:
            self.output_dir_line_edit.setText(output_dir_path)
        if logo_file_path != None:
            self.set_logo_file_line_edit.setText(logo_file_path)

        if project_name != None:
            self.project_name_line_edit.setText(project_name)
        if artist_name != None:
            self.artist_name_line_edit.setText(artist_name)
        if shot_name != None:
            self.shot_name_line_edit.setText(shot_name)

        if checkbox_state != None:
            self.enable_logo_checkbox.setChecked(checkbox_state)


    def update(self):
        print('update function started')
        self.save_prefs()
        print('update function finished')

    def save_prefs(self):

        
        source_file_path = self.filepath_field.text()
        output_dir_path = None
        logo_file_path = self.set_logo_file_line_edit.text()
        checkbox_state = self.enable_logo_checkbox.isChecked()
        project_name = self.project_name_line_edit.text()
        artist_name = self.artist_name_line_edit.text()
        shot_name = self.shot_name_line_edit.text()

        functions.update_preference(name='source_file_path', value=source_file_path)
        functions.update_preference(name ='output_dir_path' , value = output_dir_path)
        functions.update_preference(name = 'logo_file_path', value = logo_file_path)
        functions.update_preference(name = 'checkbox_state', value = checkbox_state)
        functions.update_preference(name = 'project_name', value = project_name)
        functions.update_preference(name = 'artist_name', value = artist_name)
        functions.update_preference(name = 'shot_name', value = shot_name)


    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        return separator

if __name__ == '__main__':
    
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    window = Encoding_Window()
    window.show()
    app.exec_()
    

def show():
    window = Encoding_Window()
    window.show()
