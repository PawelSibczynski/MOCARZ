import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QTextEdit, QFileDialog, \
                            QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QSize, pyqtSlot

from MCF import Converter


Converter = Converter()  # instance of MCF converter backend class

class App(QWidget):
    ''' Main GUI window class'''
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("MCF - Monte Carlo n-particle F-tally output converter")
        self.setGeometry(200, 200, 500, 500)
        self.setMinimumSize(QSize(320, 240))        
        
        self.btn_openF4 = QPushButton("F4 output to F8 input", self)

        self.LabelCell = QLabel(self)
        self.LabelCell.setText("Cell selection:")

        self.LineEditCell = QLineEdit(self)
        self.LineEditCell.setText(str(2))
        cellText = self.LineEditCell.text()

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
        self.layout.addWidget(self.LabelCell)
        self.layout.addWidget(self.LineEditCell)
        self.layout.addWidget(self.LabelColSelect)
        self.layout.addWidget(self.LineEditColumnSelect)
        self.layout.addWidget(self.LabelImpDesc)
        self.layout.addWidget(self.TextBoxImportances)




        def _F4toF8Wrapper():
            '''
            Wrapper around F4toF8 converter function with QFileDialog.
            Method of MCF class.
            '''

            fileList = QFileDialog.getOpenFileNames()

            Converter.F4toF8(fileList, cellText, ImpStr, colText)

        self.btn_openF4.clicked.connect(_F4toF8Wrapper)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_run = App()
    app_run.show()
    sys.exit(app.exec_())
    