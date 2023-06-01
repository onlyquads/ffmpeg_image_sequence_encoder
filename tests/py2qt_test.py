import sys
import os
import codecs
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog


os.environ['QT_MAC_WANTS_LAYER'] = '1'

app = QApplication(sys.argv)



class Test(QtWidgets.QWidget):
    def __init__(self):
        
        super(Test, self).__init__(None, QtCore.Qt.Tool)
        self.label = QtWidgets.QLabel('FFmpeg Sequence Encoder')
        self.label = QtWidgets.QLabel('Select any image from .exr sequence')
        


        self.button = QtWidgets.QPushButton('press me')
        self.button.released.connect(self.call_button_pressed)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def call_button_pressed(self):
        QFileDialog.getOpenFileName()
        self.label.setText(codecs.encode('ABBO !', 'rot_13'))




window = Test()
window.show()

# Start the event loop.
app.exec_()
