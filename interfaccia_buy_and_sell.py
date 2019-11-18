# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 12:31:15 2019

@author: themr
"""
import engine
from PyQt5.QtWidgets import QCheckBox,QComboBox, QTableWidget, QTableWidgetItem, QApplication, QWidget, QPushButton, QCalendarWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QLineEdit, QMessageBox, QMainWindow
from PyQt5.QtCore import pyqtSlot, QDate, Qt
from PyQt5.QtGui import QIcon, QPixmap
import sys
from functools import partial
import time
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
import user_account
import indicatorWidgets as iw
import json
import numpy as np
import matplotlib.pyplot as plt
import methods
import methodWidgets as mw

#data_extractor=engine.DataExtractor("")#.Data_extractor()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1525, 881)
        
        #parte crea 
#        self.buyStrategy=""
#        self.sellStrategy=""
        self.date_end = ""
        self.date_start = ""
        self.data_extractor=""
        self.engine=""
        self.filename=""
        
        #account
        self.user = user_account.User()
        self.saldo=0
        self.investimento=0
        self.investimento_perc=0
        self.commissioni=0
    
        
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
        self.label_4.setGeometry(QtCore.QRect(50, 120, 310, 50))
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
        
        #draw candles button
        self.pushButton_draw_candles = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_draw_candles.setGeometry(QtCore.QRect(40, 840, 100, 31))
        self.pushButton_draw_candles.setObjectName("draw_candles")   
        self.pushButton_draw_graph = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_draw_graph.setGeometry(QtCore.QRect(150, 840, 100, 31))
        self.pushButton_draw_graph.setObjectName("draw_graphs")   
        self.lineEdit_TP = QtWidgets.QLineEdit(self.centralwidget) 
        self.lineEdit_TP.setGeometry(QtCore.QRect(260, 840, 40, 22))
        self.lineEdit_TP.setObjectName("lineEdit_TP")
        #inizia tab
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(440, 40, 1391, 902))
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
        
        #tabella BUY layers
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(140, 50, 631, 251))
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setColumnCount(4)
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
        self.tableWidget.setEditTriggers
        self.tableWidget.verticalHeader().setHighlightSections(True)#
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
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
        
        self.pushButton_openlayer2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_openlayer2.setGeometry(QtCore.QRect(590, 330, 93, 28))
        self.pushButton_openlayer2.setObjectName("pushButton_openlayer2")  
        
        #tabella buy risultati
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_2.setGeometry(QtCore.QRect(140, 490, 631, 251))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setLineWidth(1)
        self.tableWidget_2.setAutoScroll(True)
        self.tableWidget_2.setProperty("showDropIndicator", True)
        self.tableWidget_2.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setCornerButtonEnabled(True)
        self.tableWidget_2.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)    
        header = self.tableWidget_2.horizontalHeader()       

        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents) 
        
        
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(430, 20, 55, 16))
        self.label.setObjectName("label")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(210, 460, 55, 16))
        self.label_13.setObjectName("label_13")
  
        self.pushButton_plot_buy = QtWidgets.QPushButton(self.tab)
        self.pushButton_plot_buy.setGeometry(QtCore.QRect(790, 330, 93, 28))
        self.pushButton_plot_buy.setObjectName("pushButton_plot_buy")  
        
        self.checkButton_wait = QtWidgets.QCheckBox(self.tab)
        self.checkButton_wait.setGeometry(QtCore.QRect(790, 230, 55, 16))
        self.checkButton_wait.setObjectName("buy and wait")
        
        #sell tab
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(310, 330, 31, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        
        
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_5.setGeometry(QtCore.QRect(470, 330, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_openlayer = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_openlayer.setGeometry(QtCore.QRect(590, 330, 93, 28))
        self.pushButton_openlayer.setObjectName("pushButton_openlayer")       
        #tabella SELL layers
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_3.setGeometry(QtCore.QRect(140, 50, 631, 251))
        self.tableWidget_3.setLineWidth(1)
        self.tableWidget_3.setAutoScroll(True)
        self.tableWidget_3.setProperty("showDropIndicator", True)
        self.tableWidget_3.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget_3.setShowGrid(True)
        self.tableWidget_3.setCornerButtonEnabled(True)
        self.tableWidget_3.setColumnCount(4)
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
        self.tableWidget_3.verticalHeader().setHighlightSections(True)
        self.tableWidget_3.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        
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
        
        #tabella sell risultati
        self.tableWidget_1 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_1.setGeometry(QtCore.QRect(140, 490, 631, 251))
        self.tableWidget_1.setObjectName("tableWidget_1")
        self.tableWidget_1.setRowCount(0)
        self.tableWidget_1.setLineWidth(1)
        self.tableWidget_1.setAutoScroll(True)
        self.tableWidget_1.setProperty("showDropIndicator", True)
        self.tableWidget_1.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget_1.setShowGrid(True)
        self.tableWidget_1.setCornerButtonEnabled(True)
        self.tableWidget_1.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_1.setHorizontalHeaderItem(3, item)          
        header = self.tableWidget_1.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)        
        
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(430, 20, 55, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(210, 460, 55, 16))
        self.label_12.setObjectName("label_12")
        
        self.tabWidget.addTab(self.tab_2, "")
        
        #tab grafici
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")  
        
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_3)
        self.label_img = QLabel(self.tab_3)
#        self.label_img.setGeometry(QtCore.QRect(25, 51, 1020, 1041))
        self.label_img.move(-50,0)
        self.label_img.resize(1500,900)
        self.label_img.setObjectName("graphicsView")
#        self.pushButton_8 = QtWidgets.QPushButton(self.tab_3)
#        self.pushButton_8.setGeometry(QtCore.QRect(780, 730, 93, 28))
#        self.pushButton_8.setObjectName("pushButton_8")
                   
        
        #risultati
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")        
        self.tableWidget_4 = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_4.setGeometry(QtCore.QRect(40, 50, 1303, 801))
        self.tableWidget_4.setLineWidth(1)
        self.tableWidget_4.setAutoScroll(True)
        self.tableWidget_4.setProperty("showDropIndicator", True)
        self.tableWidget_4.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget_4.setShowGrid(True)
        self.tableWidget_4.setCornerButtonEnabled(True)
        self.tableWidget_4.setColumnCount(8)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(7, item)
        self.tableWidget_4.verticalHeader().setHighlightSections(True)        
        
        header = self.tableWidget_4.horizontalHeader()       
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
#        
        ##### user account
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")        

#        self.label_14 = QtWidgets.QLabel(self.tab_5)
#        self.label_14.setGeometry(QtCore.QRect(20, 60, 91, 16))
#        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.tab_5)
        self.label_15.setGeometry(QtCore.QRect(20, 40, 65, 16))
        self.label_15.setObjectName("label_15")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_9.setGeometry(QtCore.QRect(300, 40, 93, 21))
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_16 = QtWidgets.QLabel(self.tab_5)
        self.label_16.setGeometry(QtCore.QRect(110, 40, 55, 16))
        self.label_16.setObjectName("label_16")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_6.setGeometry(QtCore.QRect(220, 40, 71, 22))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_17 = QtWidgets.QLabel(self.tab_5)
        self.label_17.setGeometry(QtCore.QRect(110, 80, 41, 16))
        self.label_17.setObjectName("label_17")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_7.setGeometry(QtCore.QRect(220, 80, 71, 22))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_18 = QtWidgets.QLabel(self.tab_5)
        self.label_18.setGeometry(QtCore.QRect(20, 80, 91, 16))
        self.label_18.setObjectName("label_18")
        self.pushButton_10 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_10.setGeometry(QtCore.QRect(300, 80, 131, 21))
        self.pushButton_10.setObjectName("pushButton_10")
        self.radioButton = QtWidgets.QRadioButton(self.tab_5)
        self.radioButton.setGeometry(QtCore.QRect(300, 110, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab_5)
        self.radioButton_2.setGeometry(QtCore.QRect(300, 135, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_19 = QtWidgets.QLabel(self.tab_5)
        self.label_19.setGeometry(QtCore.QRect(110, 180, 55, 16))
        self.label_19.setObjectName("label_19")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_8.setGeometry(QtCore.QRect(220, 180, 71, 22))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.label_20 = QtWidgets.QLabel(self.tab_5)
        self.label_20.setGeometry(QtCore.QRect(20, 180, 81, 16))
        self.label_20.setObjectName("label_20")
        self.pushButton_11 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_11.setGeometry(QtCore.QRect(300, 180, 141, 21))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_12.setGeometry(QtCore.QRect(50, 270, 141, 21))
        self.pushButton_12.setObjectName("pushButton_12")
        self.label_21 = QtWidgets.QLabel(self.tab_5)
        self.label_21.setGeometry(QtCore.QRect(250, 270, 131, 16))
        self.label_21.setObjectName("label_21")
        self.pushButton_save = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_save.setGeometry(QtCore.QRect(600, 180, 141, 21))
        self.pushButton_plot_results = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_plot_results.setGeometry(QtCore.QRect(800, 180, 161, 21))
#        self.tableWidget_4.setGeometry(QtCore.QRect(40, 50, 803, 641))
        self.tableWidget5 = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget5.setGeometry(QtCore.QRect(80, 350, 1251, 321))
        self.tableWidget5.setLineWidth(1)
        self.tableWidget5.setAutoScroll(True)
        self.tableWidget5.setProperty("showDropIndicator", True)
        self.tableWidget5.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableWidget5.setShowGrid(True)
        self.tableWidget5.setCornerButtonEnabled(True)
        self.tableWidget5.setColumnCount(13)
        self.tableWidget5.setObjectName("tableWidget")
        self.tableWidget5.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(3, item)    
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(6, item)  
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(7, item)  
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(8, item)  
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(10, item)  
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(11, item)  
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget5.setHorizontalHeaderItem(12, item)          
        
        header = self.tableWidget5.horizontalHeader() 
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeToContents)
        ###fine  user account
        
        
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
        self.pushButton_openlayer2.setText(_translate("MainWindow", "Open layer"))
        self.pushButton_draw_candles.setText(_translate("MainWindow", "Draw candles"))
        self.pushButton_draw_graph.setText(_translate("MainWindow", "Draw graph"))
        #tabella buy layers
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Valido"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Attivo"))
        
        self.label_8.setText(_translate("MainWindow", "Riga 2:"))
        self.pushButton_3.setText(_translate("MainWindow", "Inverti righe"))
        self.label_7.setText(_translate("MainWindow", "Riga:"))
        self.pushButton_2.setText(_translate("MainWindow", "Add layer"))        
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#00aa00;\">BUY</span></p></body></html>"))
        self.label_13.setText(_translate("MainWindow", "Risultati:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "BUY"))
        self.pushButton_5.setText(_translate("MainWindow", "Remove layer"))
        self.pushButton_openlayer.setText(_translate("MainWindow", "Open layer"))
        self.pushButton_plot_buy.setText(_translate("MainWindow", "Plot buy strategy"))
        self.checkButton_wait.setText(_translate("MainWindow", "Buy and Wait"))
        #tabella buy risultati
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Strategia"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Timestamp"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Data"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Successo"))
        
        #tabella sell layers
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Valido"))
        item = self.tableWidget_3.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Attivo"))

        #tabella sell risultati
        item = self.tableWidget_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Strategia"))
        item = self.tableWidget_1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Timestamp"))
        item = self.tableWidget_1.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Data"))
        item = self.tableWidget_1.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Successo"))
        
        self.label_9.setText(_translate("MainWindow", "Riga 2:"))
        self.pushButton_6.setText(_translate("MainWindow", "Inverti righe"))
        self.label_10.setText(_translate("MainWindow", "Riga:"))
        self.pushButton_7.setText(_translate("MainWindow", "Add layer"))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#aa0000;\">SELL</span></p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "Risultati:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "SELL"))
        
        
        #tab parte grafica
#        self.pushButton_8.setText(_translate("MainWindow", "Save image"))                        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Grafici"))
                
        #tab risultati
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Risultati"))  
        item = self.tableWidget_4.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Strategy"))
        item = self.tableWidget_4.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Layer"))
        item = self.tableWidget_4.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Method"))
        item = self.tableWidget_4.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Indicator"))
        item = self.tableWidget_4.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Timestamp"))
        item = self.tableWidget_4.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget_4.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Timeperiod"))
        item = self.tableWidget_4.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Result"))
        
        #user account
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "User account")) 
                
#        self.label_14.setText(_translate("MainWindow", "User Account"))
        self.label_15.setText(_translate("MainWindow", "Saldo:"))
        self.pushButton_9.setText(_translate("MainWindow", "modifica saldo"))
        self.label_16.setText(_translate("MainWindow", "0"))
        self.label_17.setText(_translate("MainWindow", "0"))
        self.label_18.setText(_translate("MainWindow", "Investimento:"))
        self.pushButton_10.setText(_translate("MainWindow", "modifica investimento"))
        self.radioButton.setText(_translate("MainWindow", "percentuale"))
        self.radioButton_2.setText(_translate("MainWindow", "somma"))
        self.label_19.setText(_translate("MainWindow", "0"))
        self.label_20.setText(_translate("MainWindow", "Commissioni:"))
        self.label_21.setText(_translate("MainWindow", "Risultato:  0"))
        self.pushButton_11.setText(_translate("MainWindow", "modifica commissioni"))
        self.pushButton_12.setText(_translate("MainWindow", "calcola rendimento"))
        self.pushButton_save.setText(_translate("MainWindow", "salva risultati"))
        self.pushButton_plot_results.setText(_translate("MainWindow", "visualizza risultati"))
        item = self.tableWidget5.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name Buy"))
        item = self.tableWidget5.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Timestamp"))
        item = self.tableWidget5.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget5.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Price"))
        item = self.tableWidget5.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Quantity"))
        item = self.tableWidget5.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Cost"))
        item = self.tableWidget5.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Name Sell"))
        item = self.tableWidget5.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Timestamp"))
        item = self.tableWidget5.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget5.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Price"))
        item = self.tableWidget5.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "Quantity"))
        item = self.tableWidget5.horizontalHeaderItem(11)
        item.setText(_translate("MainWindow", "Entry"))
        item = self.tableWidget5.horizontalHeaderItem(12)
        item.setText(_translate("MainWindow", "Result"))
        #fine user account
        
        
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
        
        #draw candles
        self.pushButton_draw_candles.clicked.connect(self.drawCandles)#
        self.pushButton_draw_graph.clicked.connect(self.drawGraph)
        self.pushButton_plot_buy.clicked.connect(self.drawBuyStrategy)
        #crea e rimuovi e  apri layers nella tabella
        self.pushButton_2.clicked.connect(partial(self.addLayer, tag=1))
        self.pushButton_7.clicked.connect(partial(self.addLayer, tag=2))
        self.pushButton_4.clicked.connect(partial(self.removeLayer, tag=1))
        self.pushButton_5.clicked.connect(partial(self.removeLayer, tag=2))
        self.pushButton_3.clicked.connect(partial(self.invertiLayer, tag=1))
        self.pushButton_6.clicked.connect(partial(self.invertiLayer, tag=2))   
        
        self.tableWidget_3.cellDoubleClicked.connect(self.layerMethodsSell)
        self.tableWidget.cellDoubleClicked.connect(self.layerMethodsBuy)
        
        self.pushButton_openlayer.clicked.connect(partial(self.openLayer, tag=2))
        self.pushButton_openlayer2.clicked.connect(partial(self.openLayer, tag=1))
        self.pushButton.clicked.connect(self.launchStrategy)
    
   
        #user account 
        self.pushButton_9.clicked.connect(self.changeSaldo)
        self.pushButton_10.clicked.connect(self.changeInvestimento)
        self.pushButton_11.clicked.connect(self.changeCommissioni)
        self.pushButton_12.clicked.connect(self.calcolaRendimento)
        self.pushButton_save.clicked.connect(self.saveResults)
        self.pushButton_plot_results.clicked.connect(self.plotResults)


    def plotResults(self):
        print(self.user.risultati)
        ricavi=[]
        gain=[]
        inv=[]
        for x in self.user.risultati:
            inv.append(x["invested"])
            gain.append(x["gain"])
        print(ricavi, gain, inv)
        plt.plot(np.asarray(gain), label="gain")
        plt.plot(np.asarray(inv), label="investment")
        plt.legend()
        plt.show()      
        
        
    def saveResults(self):
        risultato = {}
        risultato["data_inizio"] = str(datetime.datetime.fromtimestamp(int(self.date_start)))
        risultato["data_fine"] = str(datetime.datetime.fromtimestamp(int(self.date_end)))
        risultato["buying stratety"]={}
        for x in self.layers_buy:
            risultato["buying stratety"][x.name]={}
            for y in x.methods:
                risultato["buying stratety"][x.name][y.complete_name]=[]
                risultato["buying stratety"][x.name][y.complete_name].append(y.getNames())
        risultato["selling stratety"]={}
        for x in self.layers_sell:
            risultato["selling stratety"][x.name]={}
            for y in x.methods:
                risultato["selling stratety"][x.name][y.complete_name]=[]
                risultato["selling stratety"][x.name][y.complete_name].append(y.getNames())
        risultato["investment"]=self.label_17.text()
        risultato["return"]= self.label_21.text()
        try:
            with open("saved_results.json", "r") as f:               
                data=json.load(f)
                data["results"].append(risultato) 
                with open ("saved_results.json", "w") as f2:
                    json.dump(data, f2)
        except:
            with open ("saved_results.json", "w") as f2:
                data={}
                data["results"]=[]
                data["results"].append(risultato) 
                json.dump(data, f2)
                
        
    def drawBuyStrategy(self):
        drawer = engine.Drawer(self.data_extractor)
        drawer.drawStrategy(self.date_start,self.date_end)          

        
    def drawGraph(self):
        TP=self.lineEdit_TP.text()
        if TP=="" or TP==None:
            TP=1440
        else:
            TP=int(TP)       
        drawer = engine.Drawer(self.data_extractor)
        drawer.drawGraph(TP)    
        
        
    def drawCandles(self):
        TP=self.lineEdit_TP.text()
        if TP=="" or TP==None:
            TP=1440
        else:
            TP=int(TP)
        print(TP)
        drawer = engine.Drawer(self.data_extractor)
        drawer.drawCandles(TP)
#        except:
#            print("some error")
#            return
        
    def openLayer(self, tag):
        m=""
        if tag==2:
            selectedRow = self.tableWidget_3.selectedItems()[0]
            rowPosition=selectedRow.row()
            m = self.layers_sell[rowPosition-1]
        else:
            selectedRow = self.tableWidget.selectedItems()[0]
            rowPosition=selectedRow.row() 
            m = self.layers_buy[rowPosition-1]

        m.show()

    def changeSaldo(self):
        self.saldo= self.lineEdit_6.text()
        self.user.saldo= self.lineEdit_6.text()
        self.label_16.setText(self.lineEdit_6.text())
        
    def changeInvestimento(self):
        if self.radioButton.isChecked():
            self.investimento=(float(self.saldo)*float(self.lineEdit_7.text()))/100
        else:
            self.investimento= float(self.lineEdit_7.text())  
        self.user.investimento=self.investimento
        self.label_17.setText(str(self.investimento))      

         
    def changeCommissioni(self):
        self.commissioni= self.lineEdit_8.text()
        self.user.commissioni= self.lineEdit_8.text()
         
    def calcolaRendimento(self):
        self.operazioni = self.user.calcolaInvestimento()
        
        inv=self.investimento
#        diz={}
        somma=0
#        ricavi=[]
        for i,x in enumerate(self.user.dati_result):
            diz={}
            name_b = "buy "+str(i+1)
            name_s = "sell "+str(i+1)
            time_b = x[0][0]
            date_b = datetime.datetime.fromtimestamp(int(time_b)) 
            time_s = x[1][0]
            date_s = datetime.datetime.fromtimestamp(int(time_s)) 
            price_b = x[0][1]
            price_s = x[1][1]
            bought=float(inv)/float(price_b)
            sold_at = float(bought)*float(price_s)
            sold_amount=sold_at/float(price_s)
            ricavo=float(sold_at)-float(inv)       
            
#            ricavi.append(ricavo)
            rowPosition = self.tableWidget5.rowCount()
            self.tableWidget5.insertRow(rowPosition)
            self.tableWidget5.setItem(rowPosition,0, QTableWidgetItem(name_b))
            self.tableWidget5.setItem(rowPosition,1, QTableWidgetItem(str(time_b)))
            self.tableWidget5.setItem(rowPosition,2, QTableWidgetItem(str(date_b)))
            self.tableWidget5.setItem(rowPosition,3, QTableWidgetItem(str(price_b)))
            self.tableWidget5.setItem(rowPosition,4, QTableWidgetItem(str(bought)))
            self.tableWidget5.setItem(rowPosition,5, QTableWidgetItem(str(inv)))
            self.tableWidget5.setItem(rowPosition,6, QTableWidgetItem(name_s))
            self.tableWidget5.setItem(rowPosition,7, QTableWidgetItem(str(time_s)))
            self.tableWidget5.setItem(rowPosition,8, QTableWidgetItem(str(date_s)))
            self.tableWidget5.setItem(rowPosition,9, QTableWidgetItem(str(price_s)))
            self.tableWidget5.setItem(rowPosition,10, QTableWidgetItem(str(sold_amount)))
            self.tableWidget5.setItem(rowPosition,11, QTableWidgetItem(str(sold_at)))
            self.tableWidget5.setItem(rowPosition,12, QTableWidgetItem(str(ricavo)))          
            
            diz["name_buy"]=name_b
            diz["time_buy"]=time_b
            diz["date_buy"]=date_b
            diz["price_buy"]=price_b
            diz["amount_buy"]=bought
            diz["invested"]=inv
            diz["name_sell"]=name_s
            diz["time_sell"]=time_s
            diz["date_sell"]=date_s
            diz["price_sell"]=price_s
            diz["amount_sell"]=sold_amount
            diz["return"]=sold_at
            diz["gain"]=ricavo
            self.user.risultati.append(diz)
            inv=float(inv)+ricavo
            somma+=ricavo
        
        self.saldo=float(self.saldo)+somma
        self.label_16.setText(str(self.saldo))
        self.label_21.setText("Ricavo: "+str(somma))
#        a=plt.plot(np.asarray(ricavi))
#        plt.show()
    def checkFile(self):
        try:
            with open(self.filename, "r") as f:
                f.readline()
                s = f.readline()
                s=s.split(",")[0]
                s=s.replace("\"", "")
                print("1--"+s)
                self.date_start=int(s)
                date1 = datetime.datetime.fromtimestamp(int(s))           
                lines=f.readlines()
                s=lines[-3]
                s=s.split(",")[0]
                s=s.replace("\"", "")
                self.date_end=int(s)
                print("2--"+s)
                date2 = datetime.datetime.fromtimestamp(int(s))  
            return str(date1), str(date2)
        except:
            return "there is a problem <br>with the file format", ""
        
        
    def launchStrategy(self): 
        
        for x in self.layers_buy:
            for y in x.methods:
                y.reset(self.data_extractor)
        for x in self.layers_sell:
            for y in x.methods:
                y.reset(self.data_extractor)       
                
        if not self.checkButton_wait.isChecked():
            self.engine.lists_for_plot=[]
            self.data_extractor.indicators_results=[]
            
            strategyList=[]
    #        timedistance = self.date_end-self.date_start
            for l in self.layers_buy:
                print("layer",l)
                methodSet=set()
                for m in l.methods: 
                    print("method",m)
                    methodSet.add(m.instance)
                    print(methodSet)
                strategyList.append(methodSet)
            self.buyStrategy = engine.Strategy(strategyList)
            
            strategyList=[]
            for l in self.layers_sell:
                methodSet=set()
                for m in l.methods:                
                    methodSet.add(m.instance)
                strategyList.append(methodSet)
            self.sellStrategy = engine.Strategy(strategyList)
            
            self.engine.findBuySignal(self.buyStrategy)
            self.engine.last_timestamp=self.date_start
#            self.data_extractor.timestamp=self.date_start
            self.engine.findSellSignal(self.sellStrategy)
            self.engine.compareBuyAndSell()
            filename, compared =self.engine.saveResults()
            engine.drawResults(filename, "buy")
    
            
            self.user.calcola(self.engine.completed_strategies,self.filename)
            self.setDataTables()
            self.addImage()
            
            self.data_extractor.indicators_results=self.engine.lists_for_plot
        else:
            strategyList=[]
            self.data_extractor.indicators_results=[]
            for l in self.layers_buy:
                methodSet=set()
                for m in l.methods:                
                    methodSet.add(m.instance)
                strategyList.append(methodSet)
            self.buyStrategy = engine.Strategy(strategyList)
            segnali=self.engine.buyAndWait(self.buyStrategy, 50)
            print(segnali)
#        print(self.engine.lists_for_plot)
#        print("*********************************************************************************")
#        print(self.data_extractor.indicators_results)
        
        #reset values
        self.engine.last_timestamp=self.date_start
        self.engine.buy_results=[]
        self.engine.sell_results=[]
        self.engine.compareBuyAndSell=[]
        self.engine.completed_strategies=[]
        
        self.data_extractor.TP_files={}
        self.data_extractor.TP_files_csv={}
#        self.data_extractor.timestamp=self.date_start  
        
        
    def addImage(self):
        pixmap = QPixmap('buy.png')
        self.label_img.setPixmap(pixmap)
        self.label_img.setPixmap(pixmap.scaled(self.label_img.size())) 
        
    def setDataTables(self):

        buy=self.engine.buy_results
        sell=self.engine.sell_results
        results=self.engine.results
#        comp=self.engine.completed_strategies
        
        strategy_name=""
        layer_name=""
        method_name=""
        for strategy in results.items():
            strategy_name=strategy[0]
            for layer in strategy[1].items():
                if layer[0]!="timestamp":
                    layer_name=layer[0]
                    for method in layer[1]:                        
                        if len(method)>2:                        
                            method_name=method["method-name"]
                            result=method["result"]
                            timestamp=method["timestamp"]
                            date=datetime.datetime.fromtimestamp(int(timestamp))
                            timeperiod=method["timeperiod"]
                            for ind in method.keys():
                                if ind[0:3]=="ind":
                                    ind_name=ind+": "+method[ind]
                                    rowPosition = self.tableWidget_4.rowCount()
                                    self.tableWidget_4.insertRow(rowPosition)
                                    self.tableWidget_4.setItem(rowPosition,0, QTableWidgetItem(strategy_name))
                                    self.tableWidget_4.setItem(rowPosition,1, QTableWidgetItem(layer_name))
                                    self.tableWidget_4.setItem(rowPosition,2, QTableWidgetItem(method_name))
                                    self.tableWidget_4.setItem(rowPosition,3, QTableWidgetItem(ind_name))
                                    self.tableWidget_4.setItem(rowPosition,4, QTableWidgetItem(str(timestamp)))
                                    self.tableWidget_4.setItem(rowPosition,5, QTableWidgetItem(str(date)))
                                    self.tableWidget_4.setItem(rowPosition,6, QTableWidgetItem(timeperiod))
                                    self.tableWidget_4.setItem(rowPosition,7, QTableWidgetItem(result))
    
        buy.sort(key=lambda x : x["timestamp"])
        for strategy in buy:
            strategy_name=strategy["strategy"]
            timestamp=strategy["timestamp"]
            date=str(datetime.datetime.fromtimestamp(int(timestamp)))
            succ=strategy["succeded"]
            rowPosition = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(rowPosition)
            self.tableWidget_2.setItem(rowPosition,0, QTableWidgetItem(strategy_name))
            self.tableWidget_2.setItem(rowPosition,1, QTableWidgetItem(date))
            self.tableWidget_2.setItem(rowPosition,2, QTableWidgetItem(str(timestamp)))
            self.tableWidget_2.setItem(rowPosition,3, QTableWidgetItem(str(succ)))

        sell.sort(key=lambda x : x["timestamp"])
        for strategy in sell:
            strategy_name=strategy["strategy"]
            timestamp=strategy["timestamp"]
            date=str(datetime.datetime.fromtimestamp(int(timestamp)))
            succ=strategy["succeded"]
            rowPosition = self.tableWidget_1.rowCount()
            self.tableWidget_1.insertRow(rowPosition)
            self.tableWidget_1.setItem(rowPosition,0, QTableWidgetItem(strategy_name))
            self.tableWidget_1.setItem(rowPosition,1, QTableWidgetItem(date))
            self.tableWidget_1.setItem(rowPosition,2, QTableWidgetItem(str(timestamp)))
            self.tableWidget_1.setItem(rowPosition,3, QTableWidgetItem(str(succ)))         
            
            
    def getfile(self):
        self.dlg =QFileDialog()
        self.filename, _ =  self.dlg.getOpenFileName(None,'Open file', 'c:\\',"Image files (*.txt *.csv)")
        _filename = self.filename.split("\\")[-1]
        _filename = self.filename.split("/")[-1]
        date1, date2 = self.checkFile()
        self.label_4.setText("Selected: "+ _filename+"<br> start: "+date1+"<br> end: "+date2)


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
#        data_extractor = self.data_extractor
        check = self.data_extractor.setFile()     
        print(self.filename, self.date_start, self.date_end)
        
        if check:
            self.engine=engine.Engine(self.lineEdit.text(), self.data_extractor)
            self.engine.last_timestamp=self.date_start
#            self.data_extractor.timestamp=self.date_start
            self.label_file.setText(_translate("MainWindow", "File created successfully"))            
        else:
            self.label_file.setText(_translate("MainWindow", "File could not be created, please retry"))


    

#    @pyqtSlot()
    def layerMethodsSell(self):
        
        selectedRow = self.tableWidget_3.selectedItems()[0]
        rowPosition=selectedRow.row()
        colPosition=selectedRow.column()
        if colPosition==0:
            m = self.layers_sell[rowPosition-1]
            m.show()  
        elif colPosition==1:
            return
        elif colPosition==2:
            item = self.tableWidget_3.item(rowPosition, colPosition)
            if item.text()=="no":
                item.setText("yes")
            else:
                item.setText("no")
                
    def layerMethodsBuy(self):
        
        selectedRow = self.tableWidget.selectedItems()[0]
        rowPosition=selectedRow.row()
        colPosition=selectedRow.column()
        if colPosition==0:
            m = self.layers_buy[rowPosition-1]
            m.show()  
        elif colPosition==1:
            return
        elif colPosition==2:
            item = self.tableWidget.item(rowPosition, colPosition)
            if item.text()=="no":
                item.setText("yes")
            else:
                item.setText("no")
        
    @pyqtSlot()
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
                table.setItem(rowPosition,0, QTableWidgetItem("layer"+str(rowPosition+1)))
                table.setItem(rowPosition,2, QTableWidgetItem("no"))
                print(table.selectedItems())
                m=Layer(self.data_extractor)   
                m.name="layer"+str(rowPosition+1)
                layers.insert(rowPosition-1, m)
    
            else:
                selectedRow = table.selectedItems()[0]
                rowPosition=selectedRow.row()
                if str(self.lineEdit_2.text())!="":
                   print(str(self.lineEdit_2.text()))
                   rowPosition = int(self.lineEdit_2.text())
                table.insertRow(rowPosition)
                table.setItem(rowPosition,0, QTableWidgetItem("layer"+str(rowPosition+1)))
                table.setItem(rowPosition,2, QTableWidgetItem("no"))
                print(table.selectedItems())
                m=Layer(self.data_extractor)    
                m.name="layer"+str(rowPosition+1)
                layers.insert(rowPosition-1, m)
        except:
            return
        
#    @pyqtSlot()   
    def removeLayer(self, tag):

        if tag==1:
            table = self.tableWidget
            layers = self.layers_buy
        else:
            table=self.tableWidget_3
            layers = self.layers_sell
            
        if len(table.selectedItems())>0:
            selectedRow = table.selectedItems()[0]
            rowPosition=selectedRow.row()
            table.removeRow(rowPosition)
            layers.pop(rowPosition-1)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("seleziona il layer da rimuovere")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()



    def invertiLayer(self, tag):
        if tag==1:
            table = self.tableWidget
            layers = self.layers_buy
            edit1 = self.lineEdit_2
            edit2 = self.lineEdit_3
        else:
            table=self.tableWidget_3
            layers = self.layers_sell        
            edit1 = self.lineEdit_5
            edit2 = self.lineEdit_4
            
            
        first = int(edit1.text())
        second = int(edit2.text())
        
        layer1 = layers[first-1]
        layer2 = layers[second-1]
        
        layers[first-1]=layer2
        layers[second-1]=layer1
        
        row1=table.rowAt(first)
        row2=table.rowAt(second)

        table.insertRow(first)
        table.insertRow(second)
        
        
#    def setAllForTest(self):
        
class Layer(QWidget):
    def __init__(self, data_extractor):
        super().__init__()
        self.data_extractor=data_extractor
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
        self.table.setColumnCount(2)
        self.table.cellDoubleClicked.connect(self.layerMethods) 
        
        self.btn_add = QPushButton("add method")
        self.btn_remove = QPushButton("remove method")
        
        self.btn_add.clicked.connect(self.addMethod)
        self.btn_remove.clicked.connect(self.removeMethod)
        
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_remove)
        self.layout.addWidget(self.combo)
        
        self.setLayout(self.layout)
        
#        self.table.itemChanged[str].connect(self.changeNameMethod)
#
#
#    @pyqtSlot(str)
#    def changeNameMethod(self, arg):
#        row=self.table.selectedItems()[0].row()
#        m=self.methods[row-1]
#        m.name=arg
#        print(arg)
#        print(m.name)
        
        
#    @pyqtSlot(str)
#    def insertMethod(self):
           
            
    @pyqtSlot()
    def addMethod(self):
        rowPosition = self.table.rowCount()
        print(rowPosition)
        self.table.insertRow(rowPosition)        
        self.table.setItem(rowPosition,0, QTableWidgetItem(self.combo.currentText()))  
        arg1 = self.combo.currentText()
        
        if arg1=="price cross":
            pcw = PriceCrossWidget(self.data_extractor)
#            pcw.show()
#            self.table.setCellWidget(rowPosition,0, pcw)
            self.table.setItem(rowPosition,1, QTableWidgetItem(str(pcw.valido)))            
            self.methods.append(pcw)
            
        elif arg1=="volume extractor":
            ve = mw.VolumeExtractorWidget(self.data_extractor)
#            self.table.setCellWidget(rowPosition,0, ve)
            self.table.setItem(rowPosition,1, QTableWidgetItem(str(ve.valido)))          
            self.methods.append(ve)
            
        elif arg1=="trend spot":
            ts = mw.TrendSpotWidget(self.data_extractor)
#            self.table.setCellWidget(rowPosition,0, ts)
            self.table.setItem(rowPosition,1, QTableWidgetItem(str(ts.valido)))              
            self.methods.append(ts)
            
#        self.table.setItem(rowPosition,1, QTableWidgetItem("sssss") )
#        self.insertMethod()
#        self.combo.cu
          
    @pyqtSlot()   
    def removeMethod(self):

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
        m = self.methods[rowPosition]
#        m=self.table.cellWidget(rowPosition,0)
        print(m)
        print(m.name)
        m.show()        
 
        
    def buildWidgetCombo(self):
        d = DevelopedMethods()
        for i in d.methods:
            self.combo.addItem(i[0])
#            self.combo.addAction(i[1])

class DevelopedMethods:
    def __init__(self):
        
        self.methods = [("price cross", engine.PriceCross), 
                        ("volume extractor", methods.VolumeExtractor),
                        ("trend spot", methods.TrendSpot)]
        
        
        
        
class PriceCrossWidget(QWidget):
    def __init__(self, data_extractor):
        super().__init__()  
        self.data_extractor=data_extractor
        self.name="PriceCross"
        self.valido=False
        self.TP = 240
        
        self.instance=engine.PriceCross()
#        self.indicator1=engine.SMAClass(data_extractor, self.TP)
#        self.indicator2=engine.SMAClass(data_extractor, self.TP)
        self.crossType="above"
        self.indicatorWidget1 = SMAWidget(self.data_extractor)
        self.indicatorWidget2 = SMAWidget(self.data_extractor)
        self.setMethod()
        
        Form = self
        Form.setObjectName("Form")
        Form.resize(475, 481)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 30, 131, 16))
        
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(90, 90, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(90, 120, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(50, 210, 211, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("SMA")
        self.comboBox.addItem("CandlePrice")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(50, 180, 121, 16))
        self.label_2.setObjectName("label_2")
        
        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(50, 300, 211, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("SMA")
        self.comboBox_2.addItem("CandlePrice")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(50, 270, 121, 16))
        self.label_3.setObjectName("label_3")
        
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(290, 210, 131, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 300, 131, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(60, 60, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(320, 80, 81, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(300, 100, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText(str(self.TP))

        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(162, 380, 191, 28))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.setActions()
        
    def getNames(self):
        return [self.indicatorWidget1.instance.name, self.indicatorWidget2.instance.name ]
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Price Cross"))
        self.label.setText(_translate("Form", "Method: Price Cross"))
        self.radioButton.setText(_translate("Form", "above"))
        self.radioButton_2.setText(_translate("Form", "below"))
        self.comboBox.setItemText(0, _translate("Form", "SMA"))
        self.comboBox.setItemText(1, _translate("Form", "CandlePrice"))
        self.label_2.setText(_translate("Form", "Select first indicator"))
        self.comboBox_2.setItemText(0, _translate("Form", "SMA"))
        self.comboBox_2.setItemText(1, _translate("Form", "CandlePrice"))
        self.label_3.setText(_translate("Form", "Select second indicator"))
        self.pushButton.setText(_translate("Form", "indicator proprieties"))
        self.pushButton_2.setText(_translate("Form", "indicator proprieties"))
        self.label_4.setText(_translate("Form", "Crossing:"))
        self.label_5.setText(_translate("Form", "Time Period"))

    def setActions(self):
        self.comboBox.activated[str].connect(partial(self.selectIndicator, i=1))
        self.comboBox_2.activated[str].connect(partial(self.selectIndicator, i=2))
        
        self.pushButton.clicked.connect(partial(self.showWidget, i=1))
        self.pushButton_2.clicked.connect(partial(self.showWidget, i=2))
        
        self.lineEdit.textEdited[str].connect(self.setTP)
        self.buttonBox.accepted.connect(self.instantiateMethod)
        self.buttonBox.rejected.connect(self.close)
    
    def showWidget(self, i):
        if int(i)==1:
            self.indicatorWidget1.show()
        elif int(i)==2:
            self.indicatorWidget2.show()
            
    
    def reset(self, data_extractor):
        self.data_extractor=data_extractor
        self.instance.reset(data_extractor)
            
    def instantiateMethod(self):       
        if not self.radioButton.isChecked() and not self.radioButton_2.isChecked():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("selezionare above o below")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_() 
                          
        elif len(self.lineEdit.text())==0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("inserire un numero intero positivo")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()              
        else:
#            self.instance=engine.PriceCross()
            self.TP=self.lineEdit.text()         
            if self.radioButton.isChecked():
                self.crossType="above"
            elif self.radioButton_2.isChecked():
                self.crossType="below"
                
#            self.indicator1=self.comboBox.t
            self.complete_name=self.name+" "+str(self.TP)+" "+self.crossType
            self.setMethod()
            self.close()
            
    @pyqtSlot(str)
    def setTP(self, arg):
        try:
            self.TP=int(arg)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("inserire un numero intero positivo")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()  
               
        
    @pyqtSlot(str)
    def selectIndicator(self, arg, i):
        i=int(i)
        indicatorWidget=""

        if arg=="SMA":
            indicatorWidget=SMAWidget(self.data_extractor)
            print(arg,i)
        elif arg=="CandlePrice":
            indicatorWidget=iw.CandlePriceWidget(self.data_extractor)
            print(arg,i)  
            
        if i==1:
            self.indicatorWidget1 = indicatorWidget
            print(self.indicatorWidget1)
        elif i==2:
            self.indicatorWidget2 = indicatorWidget
            print(self.indicatorWidget2)
            
    def setMethod(self):
        self.instance=engine.PriceCross()
        self.instance.indicator1 = self.indicatorWidget1.instance
        self.instance.indicator2 = self.indicatorWidget2.instance
        self.instance.crossType = self.crossType
        self.instance.TP=self.TP
        return self
        
    
class SMAWidget(QWidget):
    def __init__(self, data_extractor):
        super().__init__()   
        
        self.data_extractor=data_extractor
        self.instance = engine.SMAClass(self.data_extractor)
        self.timeperiod=30

        Form=self
        Form.setObjectName("Form")
        Form.resize(380, 251)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(150, 70, 71, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(130, 100, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(140, 140, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(40, 180, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(120, 180, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Form)
        self.radioButton_3.setGeometry(QtCore.QRect(200, 180, 61, 20))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(Form)
        self.radioButton_4.setGeometry(QtCore.QRect(270, 180, 71, 20))
        self.radioButton_4.setObjectName("radioButton_4")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Timeperiod"))
        self.pushButton.setText(_translate("Form", "set"))
        self.radioButton_4.setText(_translate("Form", "low"))
        self.radioButton_2.setText(_translate("Form", "close"))
        self.radioButton_3.setText(_translate("Form", "high"))
        self.radioButton.setText(_translate("Form", "open"))
        
        self.pushButton.clicked.connect(self.setSMA)
        
    def reset(self, data_extractor):
        self.data_extractor=data_extractor
        self.instance.reset(data_extractor)
        
    def setSMA(self):
        t=self.lineEdit.text()
        try:
            if len(t)>0:
                
                if self.radioButton.isChecked():
                    self.instance.value_type=self.radioButton.text()
                elif self.radioButton_2.isChecked():
                    self.instance.value_type=self.radioButton_2.text()
                elif self.radioButton_3.isChecked():
                    self.instance.value_type=self.radioButton_3.text()
                elif self.radioButton_4.isChecked():
                    self.instance.value_type=self.radioButton_4.text()    
                    
                self.instance.timeperiod=int(t)
                self.instance.name+=t
                self.instance.name+=" "+self.instance.value_type
                self.close()
                
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("inserire un numero intero positivo")
            msg.setWindowTitle("MessageBox demo")
            msg.exec_()  
               
if __name__=="__main__":
    
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    win2 = QMainWindow()
    win.setupUi(win2)
    win2.show()
    
#    method = PriceCrossWidget()
#    method.show()
#    window = QWidget()
#    layout = QVBoxLayout()
#    layout.addWidget(QPushButton('Top'))
#    layout.addWidget(QPushButton('Bottom'))
#    window.setLayout(layout)
#    win.show()
#    window.show()

    sys.exit(app.exec_())
          
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SMA.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

