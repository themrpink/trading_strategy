# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:17:17 2019

@author: themr
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMessageBox
import methods 
from PyQt5 import QtWidgets
from functools import partial

class TrendSpotWidget(QWidget):
    def __init__(self, data_extractor):
        super().__init__()  
        self.data_extractor=data_extractor
        self.name="TrendSpot"
        self.valido=False
        self.TP = 240
        self.raggio=20
        self.tolleranza=0
        self.trend=False
        self.resultObject=""
        self.setMethod()
        
        Form = self
        Form.setObjectName("Form")
        Form.resize(475, 481)
        
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(180, 50, 161, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(90, 130, 81, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(190, 130, 41, 22))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(170, 290, 193, 28))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(120, 170, 51, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(190, 170, 41, 22))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(100, 210, 71, 20))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(190, 210, 41, 22))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(250, 210, 121, 21))
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(150, 360, 130, 20))
        self.label_6.setObjectName("label_6")
#        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
#        self.lineEdit_4.setGeometry(QtCore.QRect(150, 390, 130, 22))
#        self.lineEdit_4.setText("")
#        self.lineEdit_4.setObjectName("lineEdit_4")
        self.drawGraphButton = QtWidgets.QPushButton(Form)
        self.drawGraphButton.setGeometry(QtCore.QRect(150, 420, 190, 28))
        self.drawGraphButton.setObjectName("pushButton")
        
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "My indicator: Trend Spot"))
        self.label_2.setText(_translate("Form", "Time period"))
        self.label_3.setText(_translate("Form", "Raggio"))
        self.label_4.setText(_translate("Form", "Tolleranza"))
        self.label_5.setText(_translate("Form", "(Valore tra -1 e +1)"))
        self.label_6.setText(_translate("Form", "save data as:"))
        self.drawGraphButton.setText(_translate("Form", "draw graph and save data"))
        self.setActions()
        
    def setActions(self):
        self.buttonBox.accepted.connect(self.instantiateMethod)
        self.buttonBox.rejected.connect(self.close)
        self.drawGraphButton.clicked.connect(self.instance.drawAndSave)

    def reset(self, data_extractor):
        self.instance.reset(data_extractor)
        self.data_extractor=data_extractor
        self.resultObject=""
        
    def instantiateMethod(self):     
#        try:
        if len(self.lineEdit.text())==0 or len(self.lineEdit_2.text())==0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("inserire un numero intero positivo")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()              
        else:
#            self.instance=engine.PriceCross()
            self.TP=self.lineEdit.text()   
            self.raggio=self.lineEdit_2.text()
            self.tolleranza=self.lineEdit_3.text()
            self.complete_name=self.name+" "+str(self.TP)+" "+self.raggio
            self.setMethod()
            self.close()       

    def setMethod(self):
        self.instance=methods.TrendSpot(self.data_extractor)
        self.instance.raggio = self.raggio
        self.instance.tolleranza=self.tolleranza
        self.instance.TP=self.TP
        return self

    def getNames(self):
        return ["Trend Spot "+"TP:"+str(self.TP)+" raggio:"+str(self.raggio)+" tolleranza:"+str(self.tolleranza) ]
    
    
        
class VolumeExtractorWidget(QWidget):
    def __init__(self, data_extractor):
        super().__init__()  
        self.data_extractor=data_extractor
        self.name="Volume extractor"
        self.valido=False
        self.TP = 240
        self.distance=20
        
        self.setMethod()
        
        Form = self
        Form.setObjectName("Form")
        Form.resize(475, 481)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(180, 40, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(60, 120, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(80, 160, 61, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(160, 120, 41, 22))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 160, 41, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.drawGraphButton = QtWidgets.QPushButton(Form)
        self.drawGraphButton.setGeometry(QtCore.QRect(240, 170, 93, 28))
        self.drawGraphButton.setObjectName("pushButton")
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(140, 280, 193, 28))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Form)
        
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Volume Extractor"))
        self.label_2.setText(_translate("Form", "Time period"))
        self.label_3.setText(_translate("Form", "Distance"))
        self.drawGraphButton.setText(_translate("Form", "draw"))
        
        self.setActions()

    def setActions(self):
        self.buttonBox.accepted.connect(self.instantiateMethod)
        self.buttonBox.rejected.connect(self.close)
        
        self.drawGraphButton.clicked.connect(self.printGraph)        

    def printGraph(self):
        instance=methods.VolumeExtractor(self.data_extractor)
        instance.TP=int(self.lineEdit.text()) 
        instance.distance=int(self.lineEdit_2.text())
        instance.printGraph()
       
    def reset(self, data_extractor):
        self.instance.reset(data_extractor)
        self.data_extractor=data_extractor
        
        
    def instantiateMethod(self):     
#        try:
        if len(self.lineEdit.text())==0 or len(self.lineEdit_2.text())==0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("inserire un numero intero positivo")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()              
        else:
#            self.instance=engine.PriceCross()
            self.TP=self.lineEdit.text()   
            self.distance=self.lineEdit_2.text()
            self.complete_name=self.name+" "+str(self.TP)+" "+self.distance
            self.setMethod()
            self.close()

#        except:
    def getNames(self):
        return ["Volume Extractor" ]#            return
            
#            self.indicator1=self.comboBox.t
 
            
    def setMethod(self):
        self.instance=methods.VolumeExtractor(self.data_extractor)
        self.instance.distance = self.distance
        self.instance.TP=self.TP
        return self