/********************************************************************************
** Form generated from reading UI file 'GUI_qt5_design.ui'
**
** Created by: Qt User Interface Compiler version 5.15.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_GUI_QT5_DESIGN_H
#define UI_GUI_QT5_DESIGN_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_GUI_main
{
public:
    QPushButton *OpenFileDialog1_btn;
    QPushButton *OpenFileDialog2_btn;
    QPushButton *OpenFileDialog3_btn;
    QLineEdit *lineEdit;
    QListWidget *listWidget;
    QPushButton *pushButton;
    QProgressBar *progressBar;
    QLabel *label;
    QLabel *label_2;
    QLineEdit *lineEdit_2;
    QLineEdit *lineEdit_3;
    QWidget *verticalLayoutWidget;
    QVBoxLayout *verticalLayout;
    QLineEdit *lineEdit_4;
    QLabel *label_3;
    QLabel *label_4;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;

    void setupUi(QWidget *GUI_main)
    {
        if (GUI_main->objectName().isEmpty())
            GUI_main->setObjectName(QString::fromUtf8("GUI_main"));
        GUI_main->resize(863, 686);
        OpenFileDialog1_btn = new QPushButton(GUI_main);
        OpenFileDialog1_btn->setObjectName(QString::fromUtf8("OpenFileDialog1_btn"));
        OpenFileDialog1_btn->setGeometry(QRect(20, 30, 151, 23));
        OpenFileDialog2_btn = new QPushButton(GUI_main);
        OpenFileDialog2_btn->setObjectName(QString::fromUtf8("OpenFileDialog2_btn"));
        OpenFileDialog2_btn->setGeometry(QRect(20, 60, 151, 23));
        OpenFileDialog3_btn = new QPushButton(GUI_main);
        OpenFileDialog3_btn->setObjectName(QString::fromUtf8("OpenFileDialog3_btn"));
        OpenFileDialog3_btn->setGeometry(QRect(20, 90, 151, 23));
        lineEdit = new QLineEdit(GUI_main);
        lineEdit->setObjectName(QString::fromUtf8("lineEdit"));
        lineEdit->setGeometry(QRect(130, 200, 113, 20));
        listWidget = new QListWidget(GUI_main);
        listWidget->setObjectName(QString::fromUtf8("listWidget"));
        listWidget->setGeometry(QRect(485, 40, 371, 141));
        pushButton = new QPushButton(GUI_main);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setEnabled(false);
        pushButton->setGeometry(QRect(20, 120, 151, 23));
        progressBar = new QProgressBar(GUI_main);
        progressBar->setObjectName(QString::fromUtf8("progressBar"));
        progressBar->setGeometry(QRect(10, 620, 841, 23));
        progressBar->setValue(24);
        label = new QLabel(GUI_main);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(10, 600, 51, 16));
        label_2 = new QLabel(GUI_main);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(490, 20, 71, 16));
        lineEdit_2 = new QLineEdit(GUI_main);
        lineEdit_2->setObjectName(QString::fromUtf8("lineEdit_2"));
        lineEdit_2->setGeometry(QRect(130, 230, 113, 20));
        lineEdit_3 = new QLineEdit(GUI_main);
        lineEdit_3->setObjectName(QString::fromUtf8("lineEdit_3"));
        lineEdit_3->setGeometry(QRect(130, 170, 111, 20));
        verticalLayoutWidget = new QWidget(GUI_main);
        verticalLayoutWidget->setObjectName(QString::fromUtf8("verticalLayoutWidget"));
        verticalLayoutWidget->setGeometry(QRect(20, 330, 831, 241));
        verticalLayout = new QVBoxLayout(verticalLayoutWidget);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        lineEdit_4 = new QLineEdit(GUI_main);
        lineEdit_4->setObjectName(QString::fromUtf8("lineEdit_4"));
        lineEdit_4->setGeometry(QRect(130, 260, 113, 22));
        label_3 = new QLabel(GUI_main);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(30, 260, 91, 16));
        label_4 = new QLabel(GUI_main);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(30, 200, 101, 16));
        label_5 = new QLabel(GUI_main);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setGeometry(QRect(20, 230, 101, 16));
        label_6 = new QLabel(GUI_main);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setGeometry(QRect(30, 170, 101, 16));
        label_7 = new QLabel(GUI_main);
        label_7->setObjectName(QString::fromUtf8("label_7"));
        label_7->setGeometry(QRect(720, 660, 141, 16));

        retranslateUi(GUI_main);

        QMetaObject::connectSlotsByName(GUI_main);
    } // setupUi

    void retranslateUi(QWidget *GUI_main)
    {
        GUI_main->setWindowTitle(QCoreApplication::translate("GUI_main", "\"MOCARZ - MOnte CARlo analyZer v0.1\"", nullptr));
        OpenFileDialog1_btn->setText(QCoreApplication::translate("GUI_main", "Open F8 pulse height file", nullptr));
        OpenFileDialog2_btn->setText(QCoreApplication::translate("GUI_main", "Open F4 av. flux file", nullptr));
        OpenFileDialog3_btn->setText(QCoreApplication::translate("GUI_main", "Process F4 x F8", nullptr));
        lineEdit->setText(QCoreApplication::translate("GUI_main", "cell  2", nullptr));
        pushButton->setText(QCoreApplication::translate("GUI_main", "Experimental", nullptr));
        label->setText(QCoreApplication::translate("GUI_main", "Progress", nullptr));
        label_2->setText(QCoreApplication::translate("GUI_main", "Analysed files", nullptr));
        lineEdit_2->setText(QCoreApplication::translate("GUI_main", "5", nullptr));
        lineEdit_3->setText(QCoreApplication::translate("GUI_main", "1E8*100", nullptr));
        lineEdit_4->setText(QCoreApplication::translate("GUI_main", "1", nullptr));
        label_3->setText(QCoreApplication::translate("GUI_main", "F4 flux integral", nullptr));
        label_4->setText(QCoreApplication::translate("GUI_main", "Selected cell", nullptr));
        label_5->setText(QCoreApplication::translate("GUI_main", "Data col number", nullptr));
        label_6->setText(QCoreApplication::translate("GUI_main", "Flux multiplier", nullptr));
        label_7->setText(QCoreApplication::translate("GUI_main", "Pawel Sibczynski, 2022", nullptr));
    } // retranslateUi

};

namespace Ui {
    class GUI_main: public Ui_GUI_main {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_GUI_QT5_DESIGN_H
