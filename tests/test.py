import sys
from PySide2 import QtWidgets, QtGui

class FFMpegFileDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Please select the path to ffmpeg.exe:")
        layout.addWidget(label)

        self.path_line_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.path_line_edit)

        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.clicked.connect(self.browse_ffmpeg)
        layout.addWidget(browse_button)

        ok_button = QtWidgets.QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def browse_ffmpeg(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setWindowTitle("Select ffmpeg.exe")
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        file_dialog.setNameFilter("Executable Files (*.exe)")

        if file_dialog.exec_() == QtWidgets.QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            self.path_line_edit.setText(selected_file)

def get_ffmpeg_path(parent=None):
    dialog = FFMpegFileDialog(parent)
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        return dialog.path_line_edit.text()
    else:
        return None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        print(f"Selected FFmpeg path: {ffmpeg_path}")
    else:
        print("No file selected.")
    sys.exit(app.exec_())
