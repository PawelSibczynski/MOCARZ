import os
import sys
# import numpy as np
# import time
# import pyqtgraph as pg
# from PySide2 import QtGui, QtWidgets
# from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QGridLayout,QVBoxLayout #QMainWindow do obsługi okna
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit,
                               QFileDialog, QTabWidget, QTableWidget, QTableWidgetItem, QProgressBar, QVBoxLayout, 
                               QGridLayout
                               )
from PySide2.QtGui import QPalette, QColor
from PySide2.QtUiTools import QUiLoader
#from GUI_qt5_design import Ui_GUI_main
from mcnp_tgsa import My_Files   
# importuje klasę My_Files, ale musisz dla każdej metody
# z MyFiles utworzyć funkcję w Interactions, aby można było eventy wykorzystać w analizie 
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
# np progressbar
# import matplotlib
# matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import pandas as pd
import global_functions as GF

# http://pyqt.sourceforge.net/Docs/PyQt5/designer.html
# https://www.learnpyqt.com/tutorials/pyqt5-vs-pyside2/


# import sys
# from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtWidgets import QApplication, QDialog # aby działało w VS CODE, trzeba w ustawieniach 
# "Workspace settings" wkleić "python.linting.pylintArgs": ["--extension-pkg-whitelist=PyQt5"]
# from GUI_qt5_design import *

loader = QUiLoader()


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=0.1, height=0.1, dpi=100):

        self.setParent(parent)
        self.PLOT()

    
    def PLOT(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

'''
class Interactions(Ui_GUI_main): # Ui_GUI_main
    # self = 1  # zmienna statyczna, niezmennicza względem instacji klas
    def __init__(self):
        print("init dla ustawienia pierwotnych parametrów, takich jak np. sigma w gaussie czy ")
        print("lista plików. Tworzy sie zawsze gdy utworzysz instancję klasy, w której jest init")

    def LINE_EDIT_CELL(self):
        cell_name2 = self.lineEdit.text()
        return cell_name2

    def SET_F4_COLUMN(self):
        col = self.lineEdit_2.text()
        return col
    
    def SET_SOURCE_RATE(self):
        sr = self.lineEdit_3.text()
        return sr

    def GET_F4_INTEGRAL(self):
        f4int = self.lineEdit_4.text()
        return float(f4int)
    

    
    # def PLOT_WINDOW(self):
    #    A = PlotCanvas()






    def ANALYSE_F4_RET_FILE_LIST(self):
        self.listWidget.clear()
        self.file_list_widget = My_Files.Analyse_File_F4(self)[0]  # metoda wywołuje kod i zwraca
        # listę plików ([1] to nr celi)
        for item in self.file_list_widget:
            self.listWidget.addItem(os.path.basename(item))  # a potem przenosi do okienka

    def ANALYSE_FILE_F4xF8_RET_FILE_LIST(self):
        self.listWidget.clear()
        My_Files.Analyse_File_F4xF8(self)


    def ADD_BUTTONS(self):
        self.OpenFileDialog1_btn.clicked.connect(self.ANALYSE_F8_RET_FILE_LIST) # OK
        
        self.OpenFileDialog2_btn.clicked.connect(self.ANALYSE_F4_RET_FILE_LIST)
        #self.OpenFileDialog3_btn.clicked.connect(My_Files.Analyse_File_F4xF8)  # to do
        self.OpenFileDialog3_btn.clicked.connect(self.ANALYSE_FILE_F4xF8_RET_FILE_LIST)
        # trzea stworzyć funckję w klasie Interactions, która importuje analizę z My_Files
        # wtedy przez button self."Funckja w interactions" dostajemy się do analizy i
        # wtedy możemy pobierać w tejże analizie elementy z

#        self.listWidget.addItem('1')
    '''


class App(QMainWindow): #QMainWindow
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'MOCARZ - MOnte CARlo analyZer v0.11'
        self.width = 1024
        self.height = 768
        self.initUI()
        # self.show()
        self.dataProcessing = My_Files()



    def initUI(self):
        ''' Show the main window and connect events '''
        # self.window = QWidget() #  loader.load("GUI_qt5_design.ui", None)
        #grid = QtGui.QGridLayout(self.window)
        # self.window.setLayout(grid)


        self.peaks_db = pd.read_json('peak_data.json')

        print(self.peaks_db)

        self.setWindowTitle(self.title)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        central_widget = QWidget()

        # layout = QVBoxLayout()

        # grid definition
        grid = QGridLayout()
        vlayout1 = QVBoxLayout()

        # tabs definition
        tab1 = QWidget()
        tab2 = QWidget()
        
        ###
        # tab 1 widgets
        ###
        self.progressBar = QProgressBar()
        btn_read_F4_data = QPushButton('Read F4 data')
        btn_read_F8_data = QPushButton('Read F8 data')
        btn_read_F4xF8_data = QPushButton('Read F4 integral and multiply F8')
        lbl_cell = QLabel('Cell number.')
        self.ln_cell = QLineEdit('2')
        lbl_particle_count = QLabel('Particle multiplication.')
        self.ln_particle_count = QLineEdit('1E8*100')
        lbl_data_column = QLabel('Data column selection')
        ln_data_column = QLineEdit('5')
        lbl_f4_integral = QLabel('F4 Integral.')
        self.ln_f4_integral = QLineEdit('1')
        ln_log = QTextEdit('Info logger')
        
        ###
        # tab 2 widgets
        ###
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.peaks_db.columns))
        self.table.setHorizontalHeaderLabels(self.peaks_db.keys())
        self.table.setRowCount(len(self.peaks_db))

        # add data to QTableWidget
        
        for row in self.peaks_db.itertuples(): # row iterator
            for item in range(len(self.peaks_db.columns)): # iteration over columns (as integer position)
                self.table.setItem(row[0], item, QTableWidgetItem(str(row[item+1])))
        
        # GF.insert_data_to_table(self.peaks_db, self.table) # to debug
            

        # tabs and layouts
        tab_widget = QTabWidget()

        # layout with buttons running functions
        lyot_btns = QVBoxLayout()
        lyot_btns.addWidget(btn_read_F4_data)
        lyot_btns.addWidget(btn_read_F8_data)
        lyot_btns.addWidget(btn_read_F4xF8_data)

        # layout with settings used for MCNP file processing
        lyot_settings = QVBoxLayout()
        lyot_settings.addWidget(lbl_cell)
        lyot_settings.addWidget(self.ln_cell)
        lyot_settings.addWidget(lbl_particle_count)
        lyot_settings.addWidget(self.ln_particle_count)
        lyot_settings.addWidget(lbl_data_column)
        lyot_settings.addWidget(ln_data_column)
        lyot_settings.addWidget(lbl_f4_integral)
        lyot_settings.addWidget(self.ln_f4_integral)

        # add element to grid
        grid.addLayout(lyot_btns, 0, 0, 1, 1)
        grid.addLayout(lyot_settings, 2, 0, 1, 1)
        """
        grid.addWidget(Color('blue'), 0, 0, 1, 1)
        grid.addWidget(btn_read_F4_data, 0, 0, 1, 1)
        grid.addWidget(Color('green'), 1, 0, 1, 1)
        grid.addWidget(btn_read_F8_data, 1, 0, 1, 1)
        grid.addWidget(btn_read_F4xF8_data, 2, 0, 1, 1)
        grid.addWidget(lbl_cell, 3, 1, 1, 1)
        grid.addWidget(ln_cell, 3, 0, 1, 1)
        grid.addWidget(lbl_particle_count, 4, 1, 1, 1)
        grid.addWidget(ln_particle_count, 4, 0, 1, 1)
        grid.addWidget(lbl_data_column, 5, 1, 1, 1)
        grid.addWidget(ln_data_column, 5, 0, 1, 1)
        grid.addWidget(lbl_f4_integral, 6, 1, 1, 1)
        grid.addWidget(ln_f4_integral, 6, 0, 1, 1)
        """
        grid.addWidget(ln_log, 0, 2, 4, 1)
        grid.addWidget(self.progressBar, 8, 0, 1, 3) # row,column, row span, column span
        # central_widget.setLayout(grid)
        

        vlayout1.addWidget(self.table)
        tab1.setLayout(grid)
        tab2.setLayout(vlayout1)

        tab_widget.addTab(tab1, "Data processing")
        tab_widget.addTab(tab2, 'Peaks management')

        # self.window.OpenFileDialog1_btn.clicked.connect(lambda: print("clicked"))

        btn_read_F8_data.clicked.connect(self.AnalyzeF8)
        btn_read_F4_data.clicked.connect(self.AnalyzeF4)
        #self.window.OpenFileDialog2_btn.clicked.connect(self.AnalyzeF4) # obsolete 

        self.progressBar.setValue(0)


        #availableWidgets = loader.availableWidgets()
        #print(availableWidgets)

        #if not self.window:
            # print(loader.errorString())
        #    sys.exit(-1)
        # self.setCentralWidget(central_widget)
        self.setCentralWidget(tab_widget)
        print('Start application')
        # self.window.show()



    #
    # interaction methods
    # 



    

    # progressbar
    def PROGRESS(self, no_of_files):
        completed = 0

        while completed < no_of_files:
            completed += 1
            self.progressBar.setValue(completed)


    def AnalyzeF8(self):
        print("New function analysing F8")
        
        # select files
        files = self.OpenFileDialog()

        # read & analyse data from file list
        no_of_files = 1
        for f in files:
            print(f)
            self.PROGRESS(no_of_files/len(files)*100)
            no_of_files = no_of_files + 1
            self.dataProcessing.Analyse_File_F8(f, cell_name=self.ln_cell.text(),
                                                   source_rate=self.ln_particle_count.text(),
                                                   f4_integral=float(self.ln_f4_integral.text()))

    def AnalyzeF4(self):
        print("New function analysing F4")
        
        # select files
        files = self.OpenFileDialog()

        # read & analyse data from file list
        no_of_files = 1
        for f in files:
            print(f)
            self.PROGRESS(no_of_files/len(files)*100)
            no_of_files = no_of_files + 1
            self.dataProcessing.Analyse_File_F4(f, cell_name=self.window.ln_cell.text(),
                                        source_rate=self.window.ln_particle_count.text(),
                                        data_column=float(self.window.ln_data_column.text()))


    def OpenFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        list_of_files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "", "Output files (*.o);;All Files (*)", options=options)
        print(list_of_files)
        
        #for i in list_of_files:
        #    self.listWidget.addItem(i)
        
        return list_of_files


if __name__ == "__main__":
    
    APP = QApplication(sys.argv)

    ex = App()
    ex.show()

    # GUI_MAIN = QtWidgets.QWidget()
    # UI = Interactions()
    # UI.setupUi(GUI_MAIN)
    # UI.ADD_BUTTONS()
    # UI.progressBar.setValue(0) #initial values
 #   UI.PLOT_WINDOW()
    ### --- my customized layout additions here: in example, PlotCanvas --- ###
    #LAYOUT_EXTENDED = UI.verticalLayout # instancja klasy QVBoxLayout w GUI designera, bez ()!
    #PLOT_CANV = PlotCanvas(UI.verticalLayoutWidget) # a tutaj wskazujemy widgeta do QVBoxLayout
    #LAYOUT_EXTENDED.addWidget(PLOT_CANV)
    ### ---
    # GUI_MAIN.show()
    # sys.exit(APP.exec_())
    APP.exec_()
