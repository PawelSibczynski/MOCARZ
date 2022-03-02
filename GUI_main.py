import os
import sys
# import numpy as np
# import time
# import pyqtgraph as pg
from PySide2 import QtCore, QtGui, QtWidgets
# from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QGridLayout,QVBoxLayout #QMainWindow do obsługi okna
from PySide2.QtWidgets import (QApplication, QMainWindow, QFileDialog)
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

# http://pyqt.sourceforge.net/Docs/PyQt5/designer.html
# https://www.learnpyqt.com/tutorials/pyqt5-vs-pyside2/


# import sys
# from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtWidgets import QApplication, QDialog # aby działało w VS CODE, trzeba w ustawieniach 
# "Workspace settings" wkleić "python.linting.pylintArgs": ["--extension-pkg-whitelist=PyQt5"]
# from GUI_qt5_design import *

loader = QUiLoader()

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=0.1, height=0.1, dpi=100):
   #     input_file_name = None
#        fig = Figure(figsize=(width, height), dpi=dpi)
        # fig = Figure(figsize=(1, 1), dpi=dpi)
        # self.axes = fig.add_subplot(111)

        # FigureCanvas.__init__(self, fig)
        self.setParent(parent)


      #  FigureCanvas.setSizePolicy(self,
      #          QSizePolicy.Expanding,
      #          QSizePolicy.Expanding)
     #   FigureCanvas.updateGeometry(self)


#        self.PLOT(input_file_name)  # to do
        self.PLOT()


#    def PLOT(self, input_file_name): # to do
    
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
        self.title = 'MOCARZ - MOnte CARlo analyZer v0.1'
        self.width = 640
        self.height = 400
        self.initUI()
        self.dataProcessing = My_Files()

    def initUI(self):
        ''' Show the main window and connect events '''
        self.window = loader.load("GUI_qt5_design.ui", None)
        self.window.progressBar.setValue(0)

        # self.window.OpenFileDialog1_btn.clicked.connect(lambda: print("clicked")) # fajny patent
        self.window.OpenFileDialog1_btn.clicked.connect(self.AnalyzeF8)
        self.window.OpenFileDialog2_btn.clicked.connect(self.AnalyzeF4)

        availableWidgets = loader.availableWidgets()
        print(availableWidgets)

        if not self.window:
            print(loader.errorString())
            sys.exit(-1)
        self.window.show()


    #
    # interaction methods
    # 

    # progressbar
    def PROGRESS(self, no_of_files):
        completed = 0

        while completed < no_of_files:
            completed += 1
            self.window.progressBar.setValue(completed)


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
            self.dataProcessing.Analyse_File_F8(f, cell_name=self.window.lineEdit.text(),
                                                   source_rate=self.window.lineEdit_3.text(),
                                                   f4_integral=float(self.window.lineEdit_4.text()))

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
            self.dataProcessing.Analyse_File_F4(f, cell_name=self.window.lineEdit.text(),
                                        source_rate=self.window.lineEdit_3.text(),
                                        data_column=float(self.window.lineEdit_2.text()))


    def OpenFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        list_of_files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "", "Output files (*.o);;All Files (*)", options=options)
        print(list_of_files)
        
        for i in list_of_files:
            self.window.listWidget.addItem(i)
        
        return list_of_files


if __name__ == "__main__":
    APP = QtWidgets.QApplication(sys.argv) # QtWidgets importuje, nie trzeba jego wpisywać

    ex = App()


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
    sys.exit(APP.exec_())
