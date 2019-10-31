# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:31:15 2019

@author: themr
"""
import engine
from PyQt5.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem, QApplication, QWidget, QPushButton, QCalendarWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QLineEdit, QMessageBox, QMainWindow
from PyQt5.QtCore import pyqtSlot, QDate, Qt
import sys
from functools import partial
import time
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets


data_extractor=""

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1525, 881)
        
        #parte crea strategia
        self.date_end = ""
        self.date_start = ""
        self.data_extractor=""
        self.engine=""
        self.filename=""
        
        #parte crea layers
        self.layers_buy = []
        self.layers_sell = []
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 40, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 80, 55, 16))
        self.label_3.setObjectName("label_3")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(150, 80, 131, 21))
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton.setArrowType(QtCore.Qt.NoArrow)
        self.toolButton.setObjectName("toolButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 120, 211, 20))
        self.label_4.setObjectName("label_4")
        
        #start
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(40, 220, 341, 241))
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setObjectName("calendarWidget")
        #end
        self.calendarWidget_2 = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget_2.setGeometry(QtCore.QRect(40, 500, 341, 236))
        self.calendarWidget_2.setGridVisible(True)
        self.calendarWidget_2.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget_2.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget_2.setNavigationBarVisible(True)
        self.calendarWidget_2.setDateEditEnabled(True)
        self.calendarWidget_2.setObjectName("calendarWidget_2")
        
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 200, 71, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(50, 480, 71, 16))
        self.label_6.setObjectName("label_6")

        #create file button
        self.pushButton_0 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_0.setGeometry(QtCore.QRect(40, 760, 131, 51))
        self.pushButton_0.setObjectName("pushButton")
        
        #label indicating success or failure in creating file
        self.label_file = QtWidgets.QLabel(self.centralwidget)
        self.label_file.setGeometry(QtCore.QRect(50, 795, 331, 51))
        self.label_file.setObjectName("label_file")
        
        #launch button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 760, 131, 51))
        self.pushButton.setObjectName("pushButton")
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(152, 40, 131, 22))
        self.lineEdit.setObjectName("lineEdit")
        
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(440, 0, 1031, 851))
        self.tabWidget.setObjectName("tabWidget")        
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(310, 330, 31, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        
        #pulsanti BUY
        self.pushButton_4 = QtWidgets.QPushButton(self.tab)
        self.pushButton_4.setGeometry(QtCore.QRect(470, 330, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        
        #tabella BUY
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(140, 50, 631, 251))
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(260, 370, 41, 16))
        self.label_8.setObjectName("label_8")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(310, 370, 31, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(360, 370, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(270, 330, 31, 16))
        self.label_7.setObjectName("label_7")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 330, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        

        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_2.setGeometry(QtCore.QRect(140, 490, 631, 251))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(430, 20, 55, 16))
        self.label.setObjectName("label")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(210, 460, 55, 16))
        self.label_13.setObjectName("label_13")
        
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(310, 330, 31, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        
        
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_5.setGeometry(QtCore.QRect(470, 330, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        
        #tabella SELL
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_3.setGeometry(QtCore.QRect(140, 50, 631, 251))
        self.tableWidget_3.setLineWidth(1)
        self.tableWidget_3.setAutoScroll(True)
        self.tableWidget_3.setProperty("showDropIndicator", True)
        self.tableWidget_3.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget_3.setShowGrid(True)
        self.tableWidget_3.setCornerButtonEnabled(True)
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(4, item)
        self.tableWidget_3.verticalHeader().setHighlightSections(True)
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(260, 370, 41, 16))
        self.label_9.setObjectName("label_9")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(310, 370, 31, 22))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_6.setGeometry(QtCore.QRect(360, 370, 93, 28))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(270, 330, 31, 16))
        self.label_10.setObjectName("label_10")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_7.setGeometry(QtCore.QRect(360, 330, 93, 28))
        self.pushButton_7.setObjectName("pushButton_7")
        self.tableWidget_4 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_4.setGeometry(QtCore.QRect(140, 490, 631, 251))
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(0)
        self.tableWidget_4.setRowCount(0)
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(430, 20, 55, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(210, 460, 55, 16))
        self.label_12.setObjectName("label_12")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_3)
        self.graphicsView.setGeometry(QtCore.QRect(25, 51, 981, 641))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_8.setGeometry(QtCore.QRect(780, 730, 93, 28))
        self.pushButton_8.setObjectName("pushButton_8")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1525, 26))
        self.menubar.setDefaultUp(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionImport)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.actions(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Strategy name"))
        self.label_3.setText(_translate("MainWindow", "File"))
        self.toolButton.setText(_translate("MainWindow", "Open File"))
        self.label_4.setText(_translate("MainWindow", "Selected File:  None"))
        self.label_5.setText(_translate("MainWindow", "Start date:"))
        self.label_6.setText(_translate("MainWindow", "End date:"))
        self.pushButton_0.setText(_translate("MainWindow", "Create file"))
        self.pushButton.setText(_translate("MainWindow", "LAUNCH"))
        self.pushButton_4.setText(_translate("MainWindow", "Remove layer"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Number"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Valido"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Attivo"))
        self.label_8.setText(_translate("MainWindow", "Riga 2:"))
        self.pushButton_3.setText(_translate("MainWindow", "Inverti righe"))
        self.label_7.setText(_translate("MainWindow", "Riga:"))
        self.pushButton_2.setText(_translate("MainWindow", "Add layer"))
        self.label.setText(_translate("MainWindow", "BUY"))
        self.label_13.setText(_translate("MainWindow", "Risultati:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "BUY"))
        self.pushButton_5.setText(_translate("MainWindow", "Remove layer"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Number"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget_3.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Valido"))
        item = self.tableWidget_3.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Attivo"))
        self.label_9.setText(_translate("MainWindow", "Riga 2:"))
        self.pushButton_6.setText(_translate("MainWindow", "Inverti righe"))
        self.label_10.setText(_translate("MainWindow", "Riga:"))
        self.pushButton_7.setText(_translate("MainWindow", "Add layer"))
        self.label_11.setText(_translate("MainWindow", "SELL"))
        self.label_12.setText(_translate("MainWindow", "Risultati:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "SELL"))
        self.pushButton_8.setText(_translate("MainWindow", "Save image"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Grafici"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        
        
    def actions(self, MainWindow):
        #select file       
        self.toolButton.clicked.connect(self.getfile)
        
        #select dates
        self.calendarWidget.clicked[QDate].connect(partial(self.getDate,i=1))
        self.calendarWidget_2.clicked[QDate].connect(partial(self.getDate,i=2))        
        
        #crea file e istanzia il data_exctractor e l´engine
        self.pushButton_0.clicked.connect(self.instantiateEngine)
        
        #crea e rimuovi layers nella tabella
        self.pushButton_2.clicked.connect(partial(self.addLayer, i=1))
        self.pushButton_7.clicked.connect(partial(self.addLayer, i=2))
        self.pushButton_4.clicked.connect(partial(self.removeLayer, i=1))
        self.pushButton_5.clicked.connect(partial(self.removeLayer, i=2))
        
        self.tableWidget_3.cellDoubleClicked.connect(self.layerMethods)
        self.tableWidget.cellDoubleClicked.connect(self.layerMethods)
        
        
    def getfile(self):
        self.dlg =QFileDialog()
        self.filename, _ =  self.dlg.getOpenFileName(None,'Open file', 'c:\\',"Image files (*.txt *.csv)")
        _filename = self.filename.split("\\")[-1]
        _filename = self.filename.split("/")[-1]
        self.label_4.setText("Selected: "+ _filename)


    @pyqtSlot(QDate)
    def getDate(self, arg1, i):
        if i==1:            
            self.date_start=self.convertDateToTimestamp(arg1.toString(Qt.ISODate))           
            arg1.toString(Qt.ISODate)
            
        elif i==2:
            self.date_end=self.convertDateToTimestamp(arg1.toString(Qt.ISODate))

    def convertDateToTimestamp(self, date):
        return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
    

    def instantiateEngine(self):
        if self.lineEdit.text()=="" :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("non è stato inserito un nome")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()
            return 
        if self.date_end=="" or self.date_start=="":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("controlla di aver inserito le date")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()
            return    

        if self.date_start>=self.date_end:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("controlla di aver inserito le date correttamente")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()
            return  
             
        if self.filename=="":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("non hai selezionato il file")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()
            return
        
        _translate = QtCore.QCoreApplication.translate
        self.label_file.setText(_translate("MainWindow", "creating file, please wait..."))  
        
        self.data_extractor=engine.DataExtractor(self.filename, self.date_start, self.date_end, self.lineEdit.text()+".csv" )        
        data_extractor = self.data_extractor
        check = self.data_extractor.setFile()     
        
        if check:
            self.engine=engine.Engine(self.lineEdit.text(), self.data_extractor)
            self.label_file.setText(_translate("MainWindow", "File created successfully"))            
        else:
            self.label_file.setText(_translate("MainWindow", "File could not be created, please retry"))




#    @pyqtSlot()
    def layerMethods(self):
        selectedRow = self.tableWidget.selectedItems()[0]
        rowPosition=selectedRow.row()
        m = self.layers_buy[rowPosition-1]
        m.show()
        
#    @pyqtSlot()
    def addLayer(self, tag):
        
        if tag==1:
            table=self.tableWidget
            layers = self.layers_buy
        else:
            table=self.tableWidget_3
            layers = self.layers_sell
            
        try:
            if len(table.selectedItems())==0:
                rowPosition = table.rowCount()
                table.insertRow(rowPosition)
                table.setItem(rowPosition,0, QTableWidgetItem("Dai un nome al layer"))
                print(table.selectedItems())
                m=Layer()          
                layers.insert(rowPosition-1, m)
    
            else:
                selectedRow = table.selectedItems()[0]
                rowPosition=selectedRow.row()
                if str(self.lineEdit_2.text())!="":
                   print(str(self.lineEdit_2.text()))
                   rowPosition = int(self.lineEdit_2.text())
                table.insertRow(rowPosition)
                table.setItem(rowPosition,0, QTableWidgetItem("Dai un nome al layer"))
                print(table.selectedItems())
                m=Layer()          
                self.layers.insert(rowPosition-1, m)
        except:
            return
        
#    @pyqtSlot()   
    def removeLayer(sel, tag):

        if tag==1:
            table=self.tableWidget
            layers = self.layers_buy
        else:
            table=self.tableWidget_3
            layers = self.layers_sell
            
        if len(table.selectedItems())!=0:
            selectedRow = table.selectedItems()[0]
            rowPosition=selectedRow.row()
            table.removeRow(rowPosition)
            layer.pop(rowPosition-1)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("seleziona il layer da rimuovere")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()






class Layer(QWidget):
    def __init__(self):
        super().__init__()
        self.name=""
        self.attivo=True
        self.valido=True
        self.methods = []
        self.setWindowTitle("Gestisci i metodi del layer")
        self.layout = QVBoxLayout()
        
        self.combo = QComboBox()
        self.buildWidgetCombo()
             
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(1)
        self.table.cellDoubleClicked.connect(self.layerMethods) 
        
        self.btn_add = QPushButton("add method")
        self.btn_remove = QPushButton("remove method")
        
        self.btn_add.clicked.connect(self.addLayer)
        self.btn_remove.clicked.connect(self.removeLayer)
        
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_remove)
        self.layout.addWidget(self.combo)
        

        self.setLayout(self.layout)
        

    @pyqtSlot(str)
    def insertMethod(self, arg1):
        
        if arg1=="PriceCross":
            pcw = PriceCrossWidget()
            pcw.show()
            self.methods.add
    @pyqtSlot()
    def addLayer(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition,0, QTableWidgetItem(self.combo.currentText()))  
#        self.combo.cu
          
    @pyqtSlot()   
    def removeLayer(self):

        if len(self.table.selectedItems())!=0:
            selectedRow = self.table.selectedItems()[0]
            rowPosition=selectedRow.row()
            self.table.removeRow(rowPosition)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("seleziona il layer da rimuovere")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()
       

    @pyqtSlot()
    def layerMethods(self):
        selectedRow = self.table.selectedItems()[0]
        rowPosition=selectedRow.row()
        m = self.layers[rowPosition-1]
        m.show()        
        
        
    def buildWidgetCombo(self):
        d = DevelopedMethods()
        for i in d.methods:
            self.combo.addItem(i[0])
#            self.combo.addAction(i[1])

class DevelopedMethods:
    def __init__(self):
        
        self.methods = [("price cross", engine.PriceCross)]
        
        
        
        
class PriceCrossWidget(QWidget):
    def __init__(self):
        super().__init__()  
        
        sma = engine.SMAClass(data_extractor, 30)
        sma.value_type="low"
        sma.timeperiod=30
        
        sma2 = engine.SMAClass(data_extractor, 20)
        print(data_extractor.file)
        sma2.value_type="low"
        sma2.timeperiod=20        
        self.instance=engine.PriceCross(sma,sma2,"above", 50)
                    
if __name__=="__main__":
    
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    win2 = QMainWindow()
    win.setupUi(win2)
    win2.show()
#    window = QWidget()
#    layout = QVBoxLayout()
#    layout.addWidget(QPushButton('Top'))
#    layout.addWidget(QPushButton('Bottom'))
#    window.setLayout(layout)
#    win.show()
#    window.show()

    sys.exit(app.exec_())
               