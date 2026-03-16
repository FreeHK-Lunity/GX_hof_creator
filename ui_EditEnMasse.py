# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EditEnMasse.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDoubleSpinBox,
    QGridLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(603, 517)
        MainWindow.setMinimumSize(QSize(0, 400))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout.addWidget(self.pushButton_5, 3, 1, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout.addWidget(self.pushButton_4, 4, 1, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)

        self.doubleSpinBox_2 = QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setMinimum(-1.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox_2, 5, 1, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)

        self.doubleSpinBox = QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMinimum(-1.000000000000000)

        self.gridLayout.addWidget(self.doubleSpinBox, 6, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.english_textbox = QLineEdit(self.centralwidget)
        self.english_textbox.setObjectName(u"english_textbox")
        self.english_textbox.setMinimumSize(QSize(156, 0))

        self.gridLayout.addWidget(self.english_textbox, 7, 1, 1, 1)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 8, 1, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 23))
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 2, 2)

        self.searchbar = QLineEdit(self.centralwidget)
        self.searchbar.setObjectName(u"searchbar")
        self.searchbar.setMaxLength(32767)
        self.searchbar.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.searchbar, 0, 0, 1, 1)

        self.pushButton_7 = QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.gridLayout_2.addWidget(self.pushButton_7, 2, 2, 1, 1)

        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.gridLayout_2.addWidget(self.pushButton_6, 2, 1, 1, 1)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.gridLayout_2.addWidget(self.listWidget, 1, 0, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 603, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Add Bus Stop", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Set 6w 3 pages 8w 2 pages", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Set 3 pages for 6w8w", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Set 6w 2 pages 8w 1 page", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Set 2 pages for 6w8w", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Set Inbounds Section Fare", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Set Outbounds Section Fare", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Set English", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Set Autoskip", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Common Shortcuts", None))
        self.searchbar.setInputMask("")
        self.searchbar.setText("")
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Confirm", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Revert", None))
    # retranslateUi

