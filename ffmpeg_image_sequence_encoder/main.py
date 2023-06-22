
import os 
import sys
from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout,QLabel, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QFrame, QSpinBox
import functions

### FOR MAC OS WE NEED THIS LINE FOR PYTHON 2.7
os.environ['QT_MAC_WANTS_LAYER'] = '1'


class Encoding_Window(QMainWindow):
    def __init__(self):

        super(Encoding_Window, self).__init__()
        self.setWindowTitle(functions.tool_name)
        
        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Create a text field for the file path
        self.filepath_field = QLineEdit()
        layout.addWidget(self.filepath_field)
        
        # Create a browse button
        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.browse_files)
        layout.addWidget(browse_button)

        # Create a separator
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.HLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator_line)


        # Create a horizontal layout for FPS spinBox and Label

        fps_layout = QHBoxLayout()
        # Create a spinbox to set FPS
        fps_label = QLabel('Set FPS')
        fps_layout.addWidget(fps_label)

        self.fps_spinbox = QSpinBox()
        self.fps_spinbox.setMinimum(1)
        self.fps_spinbox.setValue(24)
        fps_layout.addWidget(self.fps_spinbox)

        layout.addLayout(fps_layout)



        # Create the encode button
        encode_button = QPushButton('Encode')
        encode_button.clicked.connect(self.encode_with_ffmpeg)
        layout.addWidget(encode_button)

        # Create the open directory button
        open_dir_button = QPushButton('Open Directory')
        open_dir_button.clicked.connect(self.open_dir)
        layout.addWidget(open_dir_button)

        self.setCentralWidget(central_widget)
        
    def browse_files(self):
        # Open the file browser and filter for .exr files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('EXR Sequence (*.exr *.jpg *.jpeg *.tiff *.png)')
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.filepath_field.setText(selected_files[0])

    def encode_with_ffmpeg(self):
        # Get specified FPS
        fps_value = self.fps_spinbox.text()
        # Get the file path
        file_path = self.filepath_field.text()
        # Get the input name formated with %04d and the output file
        input_file_name, output_file_name, file_extension = functions.get_in_out_files(file_path)
        print('Start encoding')
        functions.encode_with_ffmpeg(input_file_name, output_file_name, file_extension, fps_value)
    
    def open_dir(self):
        file_path = self.filepath_field.text()
        path = os.path.dirname(file_path)
        functions.open_dir(path)

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
