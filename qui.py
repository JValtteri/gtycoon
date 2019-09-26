#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.Valtteri 24.9.2019
# QUI

import sys
from PySide2.QtCore import *
from PySide2.QtGui import *

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
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(-24, 24)
        self.slider.setValue(-13)
        self.label = QLabel()

        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.connect(self.slider, SIGNAL("valueChanged(int)"),
                     lcd, SLOT("display(int)"))
        
        self.connect(self.slider, SIGNAL("valueChanged(int)"),
                     self, SIGNAL("valueChanged(int)"))

        layout = QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)

    def text(self):
        return self.label.text()

    def setRange(self, minValue, maxValue):
        if minValue < -24 or maxValue > 24 or minValue > maxValue:
            qWarning("LCDRange::setRange(%d, %d)\n"
                    "\tRange must be 0..99\n"
                    "\tand minValue must not be greater than maxValue" % (minValue, maxValue))
            return

        self.slider.setRange(minValue, maxValue)

    def setText(self, text):
        self.label.setText(text)

        #############

#
qt_app = QApplication(sys.argv)
label = QLabel(G-Tycoon)
label.show()
qt_app.excec_()
