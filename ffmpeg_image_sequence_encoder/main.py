
import os 
import sys
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QFrame
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
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_files)
        layout.addWidget(browse_button)

        # Create a separator

        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.HLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator_line)

        # Create the encode button
        encode_button = QPushButton('Encode')
        encode_button.clicked.connect(self.encode_with_ffmpeg)
        layout.addWidget(encode_button)

        # Create the open directory button
        open_dir_button = QPushButton('Open Directory')
        open_dir_button.clicked.connect(self.open_dir)
        layout.addWidget(open_dir_button)


        self._window = None

        self.setCentralWidget(central_widget)
        
    def browse_files(self):
        # Open the file browser and filter for .exr files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("EXR files (*.exr)")
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.filepath_field.setText(selected_files[0])

    def encode_with_ffmpeg(self):
        # Get the file path
        file_path = self.filepath_field.text()
        # Get the input name formated with %04d and the output file
        input_file_name, output_file_name = functions.get_in_out_files(file_path)
        print('Start encoding')
        functions.encode_with_ffmpeg(input_file_name, output_file_name)
    
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
    

def show(self):
    window = Encoding_Window()
    window.show()
