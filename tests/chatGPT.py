
import os 
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QFrame

os.environ['QT_MAC_WANTS_LAYER'] = '1'

class EncodingWindow(QMainWindow):
    def __init__(self):
        super(EncodingWindow, self).__init__()
        self.setWindowTitle("File Browser Example")
        
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

        print('Start encoding')
        path = self.filepath_field.text()
        print (path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EncodingWindow()
    window.show()
    sys.exit(app.exec_())