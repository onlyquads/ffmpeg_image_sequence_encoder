import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QLabel

import os
os.environ['QT_MAC_WANTS_LAYER'] = '1'

app = QApplication(sys.argv)
label = QLabel("<center><h1>I must have left my house at eight,<br />because I always do.</h1></center>")
label.show()
app.exec_()