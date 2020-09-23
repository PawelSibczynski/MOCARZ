import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QTextEdit, QFileDialog, \
                            QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QSize, pyqtSlot

from MCF import Converter

import matplotlib.pyplot as plt

Converter = Converter()  # instance of MCF converter backend class

class App(QWidget):
    ''' Main GUI window class'''
    def __init__(self):
        super().__init__()
        self.initUI()
        self.df = pd.DataFrame()
    
    def initUI(self):
        self.setWindowTitle("MCF - Monte Carlo n-particle F-tally output converter")
        self.setGeometry(200, 200, 500, 500)
        self.setMinimumSize(QSize(320, 240))        
        
        self.btn_openF4 = QPushButton("F4 output to F8 input", self)
        self.btnPlotData = QPushButton("Plot F4", self)

        self.LabelCell = QLabel(self)
        self.LabelCell.setText("Cell selection:")
        self.LineEditCell = QLineEdit(self)
        self.LineEditCell.setText(str(2))
        cellText = self.LineEditCell.text()

        self.LabelNPS = QLabel(self)
        self.LabelNPS.setText("Set number of histories:")
        self.LineEditNPS = QLineEdit(self)
        self.LineEditNPS.setText("1E8")
        nps = self.LineEditNPS.text()

        self.LineEditColumnSelect = QLineEdit(self)
        self.LineEditColumnSelect.setText("Delayed") # you can currently chose Prompt, Delayed and Total
        colText = self.LineEditColumnSelect.text()

        self.TextBoxImportances = QTextEdit(self)
        self.TextBoxImportances.setText(Converter.getImportancesStr(cellText))
        self.TextBoxImportances.setMinimumHeight(150)
        ImpStr = self.TextBoxImportances.toPlainText()

        self.LabelImpDesc = QLabel(self)
        self.LabelImpDesc.setText("Geometry importance description:")

        self.LabelColSelect = QLabel(self)
        self.LabelColSelect.setText("F4 column select (prompt, delayed or totat):")

        # layout
        self.layout = QVBoxLayout(self)
        self.layout.TopToBottom
        self.layout.addWidget(self.btn_openF4)
        self.layout.addWidget(self.btnPlotData)
        self.layout.addWidget(self.LabelCell)
        self.layout.addWidget(self.LineEditCell)
        self.layout.addWidget(self.LabelColSelect)
        self.layout.addWidget(self.LineEditColumnSelect)
        self.layout.addWidget(self.LabelNPS)
        self.layout.addWidget(self.LineEditNPS)
        self.layout.addWidget(self.LabelImpDesc)
        self.layout.addWidget(self.TextBoxImportances)





        def _F4toF8Wrapper():
            '''
            Wrapper around F4toF8 converter function with QFileDialog.
            Method of MCF class.
            '''
            # get params from GUI after button click
            cellText = self.LineEditCell.text()
            ImpStr = self.TextBoxImportances.toPlainText()
            nps = self.LineEditNPS.text()
            print(ImpStr)
            fileList = QFileDialog.getOpenFileNames()

            df = Converter.F4toF8(fileList, cellText, ImpStr, colText, nps)


        self.btn_openF4.clicked.connect(_F4toF8Wrapper)
        self.btnPlotData.clicked.connect(self.plot_data)
        self.show()
    

    def plot_data(self):
        df = self.df
        
        if "Delimiter" in df.columns:
            df = df.drop(columns=["Delimiter"])
        
        df = df.astype(float)
        df['Total'] = df['Total']*1E8 # in future, allow to assume other neutron fluxes
        print(df.info())
        print("Total neutrons per second:", sum(df['Total']))

        if not df.empty:
        #    print(df)
            plt.plot(df['Energy'], df['Total'])
            plt.errorbar(df['Energy'], df['Total'], yerr=df['Total']*df['Total_err'], ecolor='Black')
            plt.ylim(bottom=0.1)
            plt.yscale('log')
            plt.tight_layout()
            plt.show()
            

        else:
            print("Data has no values. Unable to plot.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_run = App()
    app_run.show()
    sys.exit(app.exec_())
    