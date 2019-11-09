# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:17:17 2019

@author: themr
"""

import indicators
from PyQt5 import QtCore, QtGui, QtWidgets


class CandlePriceWidget(QtWidgets.QWidget):
    def __init__(self, data_extractor):
        super().__init__()  
        self.data_extractor=data_extractor
        self.name="CandlePrice"
        self.valido=False    
        self.instance=indicators.CandlePrice(self.data_extractor)
        self.valueType=self.instance.valueType
        
        Form = self
        Form.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(140, 170, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.radioButton_4 = QtWidgets.QRadioButton(Form)
        self.radioButton_4.setGeometry(QtCore.QRect(270, 110, 71, 20))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(120, 110, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Form)
        self.radioButton_3.setGeometry(QtCore.QRect(200, 110, 61, 20))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(40, 110, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 20, 161, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(150, 80, 81, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.radioButton_4.setText(_translate("Form", "low"))
        self.radioButton_2.setText(_translate("Form", "close"))
        self.radioButton_3.setText(_translate("Form", "high"))
        self.radioButton.setText(_translate("Form", "open"))
        self.label.setText(_translate("Form", "Candle Price"))
        self.label_2.setText(_translate("Form", "Value Type:"))
        self.pushButton.setText(_translate("Form", "set"))
        
        self.pushButton.clicked.connect(self.setCandlePrice)
        
        
    def setCandlePrice(self):
        if self.radioButton.isChecked():
            self.instance.valueType=self.radioButton.text()
        elif self.radioButton_2.isChecked():
            self.instance.valueType=self.radioButton_2.text()
        elif self.radioButton_3.isChecked():
            self.instance.valueType=self.radioButton_3.text()
        elif self.radioButton_4.isChecked():
            self.instance.valueType=self.radioButton_4.text()          

        self.instance.name+=" "+self.instance.valueType
        self.close()