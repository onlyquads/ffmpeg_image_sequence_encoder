import os
import sys
import platform
from PySide2 import QtWidgets
from PySide2.QtWidgets import (
    QMainWindow, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit,
    QPushButton, QFileDialog, QFrame, QSpinBox, QAction)
import functions

# FOR MAC OS WE NEED THIS LINE FOR PYTHON 2.7
os.environ['QT_MAC_WANTS_LAYER'] = '1'


class Encoding_Window(QMainWindow):
    def __init__(self):

        super(Encoding_Window, self).__init__()
        self.setWindowTitle(functions.TOOL_NAME)

        self.load_ui()
        self.load_menubar()

    def load_ui(self):

        # Create a central widget and layout
        central_widget = QtWidgets.QWidget(self)

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
        central_widget.setLayout(layout)

    def load_menubar(self):
        # Add a menu bar
        menu_bar = self.menuBar()

        # MAC OS Struggle to display the menubar
        # so we disable the native support here
        menu_bar.setNativeMenuBar(platform.system() != 'Darwin')

        # Create a file menu
        file_menu = menu_bar.addMenu('File')

        # Create actions for the file menu
        set_ffmpeg_path = QAction('Set ffmpeg path', self)
        exit_action = QAction('Exit', self)

        # Add the actions to the file menu
        file_menu.addAction(set_ffmpeg_path)
        file_menu.addAction(exit_action)

        set_ffmpeg_path.triggered.connect(self.set_ffmpeg_path)
        exit_action.triggered.connect(self.close)

        # Set the menu bar to the main window
        self.setMenuBar(menu_bar)

    def browse_files(self):
        # Open the file browser and filter for supported image files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter(
            'EXR Sequence (*.exr *.jpg *.jpeg *.tiff *.png)')

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.filepath_field.setText(selected_files[0])

    def encode_with_ffmpeg(self):
        # Get specified FPS
        fps_value = self.fps_spinbox.text()
        # Get the file path
        file_path = self.filepath_field.text()
        # Get the input name formated with %04d and the output file
        input_name, output_name, ext = functions.get_in_out_files(file_path)
        # Start the encoding process
        functions.encode_with_ffmpeg(
            input_name, output_name, ext, fps_value)

    def open_dir(self):
        file_path = self.filepath_field.text()
        path = os.path.dirname(file_path)
        functions.open_dir(path)

    def set_ffmpeg_path(self):
        self.popup_ffmpeg_path()

    def popup_ffmpeg_path(self):
        ffmpeg_pref_path = functions.read_pref_file('ffmpeg_path')
        if ffmpeg_pref_path == '' or ffmpeg_pref_path is None:
            ffmpeg_pref_path = 'Not Set!'
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowTitle("Browse to FFmpeg")
        message_box.setText("Current FFmpeg executable <p>"+ffmpeg_pref_path)
        browse_button = QPushButton("Browse")
        message_box.addButton(browse_button, QMessageBox.AcceptRole)
        message_box.setStandardButtons(QMessageBox.Cancel)

        message_box.exec_()

        if message_box.clickedButton() == browse_button:
            ffmpeg_path = self.browse_to_ffmpeg()
            print("FFmpeg path confirmed:", ffmpeg_path)
            functions.write_pref_file(ffmpeg_path)
        else:
            print("FFmpeg path selection cancelled.")

    def browse_to_ffmpeg(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        # file_dialog.setNameFilter('FFmpeg Executable (*.exe)')

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            ffmpeg_path = selected_files[0]

            if ffmpeg_path:
                return ffmpeg_path
        else:
            QMessageBox.warning(
                self, "Warning", "No FFmpeg executable selected.")


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
