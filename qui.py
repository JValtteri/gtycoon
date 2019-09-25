# 
# 
# J.Valtteri 24.9.2019
# QUI

import sys
from PySide.QtCore import *
from PySide.QtGui import *

# from pyside tutorial t13

class LCDRange(QWidget):
    def __init__(self, text=None, parent=None):
        if isinstance(text, QWidget):
            parent = text
            text = None

        QWidget.__init__(self, parent)

        self.init()

        if text:
            self.setText(text)

    def init(self):
        lcd = QLCDNumber(2)
        self.slider = QSlider( ####

#
qt_app = QApplication(sys.argv)
label = QLabel(G-Tycoon)
label.show()
qt_app.excec_()

