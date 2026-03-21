# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Welc.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSplitter, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 326)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(800, 326))
        MainWindow.setMaximumSize(QSize(800, 326))
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.actionOpen_Project_Folder = QAction(MainWindow)
        self.actionOpen_Project_Folder.setObjectName(u"actionOpen_Project_Folder")
        self.actionOpen_HOF = QAction(MainWindow)
        self.actionOpen_HOF.setObjectName(u"actionOpen_HOF")
        self.actionOpen_TTL_for_Route = QAction(MainWindow)
        self.actionOpen_TTL_for_Route.setObjectName(u"actionOpen_TTL_for_Route")
        self.actionSave_to_DB = QAction(MainWindow)
        self.actionSave_to_DB.setObjectName(u"actionSave_to_DB")
        self.actionOpen_global_cfg = QAction(MainWindow)
        self.actionOpen_global_cfg.setObjectName(u"actionOpen_global_cfg")
        self.actionExport_HOF = QAction(MainWindow)
        self.actionExport_HOF.setObjectName(u"actionExport_HOF")
        self.actionGenerate_8w_6w_LCD = QAction(MainWindow)
        self.actionGenerate_8w_6w_LCD.setObjectName(u"actionGenerate_8w_6w_LCD")
        self.actionGenerate_DPIPv2 = QAction(MainWindow)
        self.actionGenerate_DPIPv2.setObjectName(u"actionGenerate_DPIPv2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.label = QLabel(self.splitter_2)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Malgun Gothic"])
        font.setPointSize(32)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setFrameShape(QFrame.Shape.Panel)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.splitter_2.addWidget(self.label)

        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.horizontalLayoutWidget = QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_4 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.splitter.addWidget(self.horizontalLayoutWidget)

        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuMap = QMenu(self.menubar)
        self.menuMap.setObjectName(u"menuMap")
        self.menuLED = QMenu(self.menubar)
        self.menuLED.setObjectName(u"menuLED")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMap.menuAction())
        self.menubar.addAction(self.menuLED.menuAction())
        self.menuFile.addAction(self.actionOpen_Project_Folder)
        self.menuFile.addAction(self.actionOpen_HOF)
        self.menuFile.addAction(self.actionSave_to_DB)
        self.menuFile.addAction(self.actionExport_HOF)
        self.menuMap.addAction(self.actionOpen_TTL_for_Route)
        self.menuMap.addAction(self.actionOpen_global_cfg)
        self.menuLED.addAction(self.actionGenerate_8w_6w_LCD)
        self.menuLED.addAction(self.actionGenerate_DPIPv2)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GX Hof Creator Menu", None))
        self.actionOpen_Project_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Project Folder", None))
        self.actionOpen_HOF.setText(QCoreApplication.translate("MainWindow", u"Open HOF", None))
        self.actionOpen_TTL_for_Route.setText(QCoreApplication.translate("MainWindow", u"Open TTL for Route", None))
        self.actionSave_to_DB.setText(QCoreApplication.translate("MainWindow", u"Save to DB", None))
        self.actionOpen_global_cfg.setText(QCoreApplication.translate("MainWindow", u"Open global.cfg", None))
        self.actionExport_HOF.setText(QCoreApplication.translate("MainWindow", u"Export HOF", None))
        self.actionGenerate_8w_6w_LCD.setText(QCoreApplication.translate("MainWindow", u"Generate 8w,6w", None))
        self.actionGenerate_DPIPv2.setText(QCoreApplication.translate("MainWindow", u"Generate DPIPv2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"GX Hof Creator", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Import from Map", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Open a GHC .db", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open HOF", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuMap.setTitle(QCoreApplication.translate("MainWindow", u"Map", None))
        self.menuLED.setTitle(QCoreApplication.translate("MainWindow", u"LED", None))
    # retranslateUi

