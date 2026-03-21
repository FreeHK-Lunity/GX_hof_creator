# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HOFView.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(729, 834)
        MainWindow.setMinimumSize(QSize(625, 834))
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
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionImport_Busstops_from_list = QAction(MainWindow)
        self.actionImport_Busstops_from_list.setObjectName(u"actionImport_Busstops_from_list")
        self.actionEric_Guesser = QAction(MainWindow)
        self.actionEric_Guesser.setObjectName(u"actionEric_Guesser")
        self.actionExport_HOF_v2 = QAction(MainWindow)
        self.actionExport_HOF_v2.setObjectName(u"actionExport_HOF_v2")
        self.actionReset_Busstop_List_IDs = QAction(MainWindow)
        self.actionReset_Busstop_List_IDs.setObjectName(u"actionReset_Busstop_List_IDs")
        self.actionEdit_En_Masse = QAction(MainWindow)
        self.actionEdit_En_Masse.setObjectName(u"actionEdit_En_Masse")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setMinimumSize(QSize(14, 279))
        self.line_2.setMaximumSize(QSize(14, 279))
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 0, 7, 7, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(126, 69))
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 8, 3, 1)

        self.pushButton_13 = QPushButton(self.centralwidget)
        self.pushButton_13.setObjectName(u"pushButton_13")
        self.pushButton_13.setMinimumSize(QSize(60, 23))
        self.pushButton_13.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_13, 2, 6, 1, 1)

        self.pushButton_8 = QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setMinimumSize(QSize(60, 23))
        self.pushButton_8.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_8, 1, 6, 1, 1)

        self.pushButton_14 = QPushButton(self.centralwidget)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setMinimumSize(QSize(60, 23))
        self.pushButton_14.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_14, 0, 10, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(126, 69))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 3, 1)

        self.pushButton_16 = QPushButton(self.centralwidget)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setMinimumSize(QSize(60, 23))
        self.pushButton_16.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_16, 2, 10, 1, 1)

        self.pushButton_11 = QPushButton(self.centralwidget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setMinimumSize(QSize(60, 23))
        self.pushButton_11.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_11, 2, 2, 1, 1)

        self.pushButton_15 = QPushButton(self.centralwidget)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setMinimumSize(QSize(60, 23))
        self.pushButton_15.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_15, 1, 10, 1, 1)

        self.pushButton_7 = QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setMinimumSize(QSize(60, 23))
        self.pushButton_7.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_7, 0, 6, 1, 1)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(125, 69))
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 0, 4, 3, 1)

        self.pushButton_22 = QPushButton(self.centralwidget)
        self.pushButton_22.setObjectName(u"pushButton_22")
        self.pushButton_22.setMinimumSize(QSize(16, 72))
        self.pushButton_22.setMaximumSize(QSize(16, 72))

        self.gridLayout.addWidget(self.pushButton_22, 0, 5, 3, 1)

        self.listWidget_3 = QListWidget(self.centralwidget)
        self.listWidget_3.setObjectName(u"listWidget_3")
        self.listWidget_3.setMinimumSize(QSize(186, 210))

        self.gridLayout.addWidget(self.listWidget_3, 6, 0, 1, 3)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(60, 23))
        self.pushButton_3.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(60, 23))
        self.pushButton_5.setMaximumSize(QSize(60, 23))

        self.gridLayout.addWidget(self.pushButton_5, 1, 2, 1, 1)

        self.listWidget_5 = QListWidget(self.centralwidget)
        self.listWidget_5.setObjectName(u"listWidget_5")
        self.listWidget_5.setMinimumSize(QSize(186, 210))

        self.gridLayout.addWidget(self.listWidget_5, 6, 8, 1, 3)

        self.pushButton_23 = QPushButton(self.centralwidget)
        self.pushButton_23.setObjectName(u"pushButton_23")
        self.pushButton_23.setMinimumSize(QSize(16, 72))
        self.pushButton_23.setMaximumSize(QSize(16, 72))

        self.gridLayout.addWidget(self.pushButton_23, 0, 1, 3, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(14, 279))
        self.line.setMaximumSize(QSize(14, 279))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 0, 3, 7, 1)

        self.listWidget_4 = QListWidget(self.centralwidget)
        self.listWidget_4.setObjectName(u"listWidget_4")
        self.listWidget_4.setMinimumSize(QSize(185, 210))

        self.gridLayout.addWidget(self.listWidget_4, 6, 4, 1, 3)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(581, 0))
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_3, 7, 0, 1, 11)

        self.pushButton_21 = QPushButton(self.centralwidget)
        self.pushButton_21.setObjectName(u"pushButton_21")
        self.pushButton_21.setMinimumSize(QSize(16, 72))
        self.pushButton_21.setMaximumSize(QSize(16, 16777215))

        self.gridLayout.addWidget(self.pushButton_21, 0, 9, 3, 1)

        self.verticalSpacer = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.toolButton_5 = QToolButton(self.centralwidget)
        self.toolButton_5.setObjectName(u"toolButton_5")
        self.toolButton_5.setMaximumSize(QSize(58, 40))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.toolButton_5.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.toolButton_5)

        self.toolButton_6 = QToolButton(self.centralwidget)
        self.toolButton_6.setObjectName(u"toolButton_6")
        self.toolButton_6.setMaximumSize(QSize(58, 40))
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        self.toolButton_6.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.toolButton_6)


        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 10, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.toolButton_7 = QToolButton(self.centralwidget)
        self.toolButton_7.setObjectName(u"toolButton_7")
        self.toolButton_7.setMaximumSize(QSize(58, 40))
        self.toolButton_7.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.toolButton_7)

        self.toolButton_8 = QToolButton(self.centralwidget)
        self.toolButton_8.setObjectName(u"toolButton_8")
        self.toolButton_8.setMaximumSize(QSize(58, 40))
        self.toolButton_8.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.toolButton_8)


        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 6, 1, 1)

        self.Search = QLineEdit(self.centralwidget)
        self.Search.setObjectName(u"Search")

        self.gridLayout.addWidget(self.Search, 4, 0, 1, 3)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 6)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(63, 25))
        self.label_3.setMaximumSize(QSize(77, 16777215))
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.pushButton_9 = QPushButton(self.centralwidget)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setMinimumSize(QSize(66, 23))
        self.pushButton_9.setMaximumSize(QSize(66, 32768))

        self.gridLayout_2.addWidget(self.pushButton_9, 1, 1, 1, 1)

        self.pushButton_12 = QPushButton(self.centralwidget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setMinimumSize(QSize(66, 23))
        self.pushButton_12.setMaximumSize(QSize(66, 32768))

        self.gridLayout_2.addWidget(self.pushButton_12, 1, 2, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(103, 64))
        self.label_4.setFont(font)

        self.gridLayout_2.addWidget(self.label_4, 1, 3, 2, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_24 = QPushButton(self.centralwidget)
        self.pushButton_24.setObjectName(u"pushButton_24")
        self.pushButton_24.setMinimumSize(QSize(78, 33))

        self.gridLayout_4.addWidget(self.pushButton_24, 0, 1, 1, 1)

        self.pushButton_18 = QPushButton(self.centralwidget)
        self.pushButton_18.setObjectName(u"pushButton_18")
        self.pushButton_18.setMinimumSize(QSize(78, 40))

        self.gridLayout_4.addWidget(self.pushButton_18, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 4, 2, 1)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_2.addWidget(self.checkBox, 1, 5, 1, 1)

        self.pushButton_10 = QPushButton(self.centralwidget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setMinimumSize(QSize(66, 23))
        self.pushButton_10.setMaximumSize(QSize(66, 34))

        self.gridLayout_2.addWidget(self.pushButton_10, 2, 1, 1, 1)

        self.pushButton_19 = QPushButton(self.centralwidget)
        self.pushButton_19.setObjectName(u"pushButton_19")
        self.pushButton_19.setMaximumSize(QSize(66, 34))

        self.gridLayout_2.addWidget(self.pushButton_19, 2, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(35, 30))
        self.pushButton.setMaximumSize(QSize(35, 30))

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(35, 30))
        self.pushButton_2.setMaximumSize(QSize(35, 30))

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 5, 1, 1)

        self.listWidget_2 = QListWidget(self.centralwidget)
        self.listWidget_2.setObjectName(u"listWidget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_2.sizePolicy().hasHeightForWidth())
        self.listWidget_2.setSizePolicy(sizePolicy)
        self.listWidget_2.setMinimumSize(QSize(221, 231))

        self.gridLayout_2.addWidget(self.listWidget_2, 3, 0, 1, 3)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(211, 351))

        self.gridLayout_2.addWidget(self.listWidget, 3, 3, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolButton_4 = QToolButton(self.centralwidget)
        self.toolButton_4.setObjectName(u"toolButton_4")
        self.toolButton_4.setMaximumSize(QSize(58, 40))
        self.toolButton_4.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.toolButton_4)

        self.toolButton_3 = QToolButton(self.centralwidget)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setMaximumSize(QSize(58, 40))
        self.toolButton_3.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.toolButton_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.pushButton_17 = QPushButton(self.centralwidget)
        self.pushButton_17.setObjectName(u"pushButton_17")
        self.pushButton_17.setMinimumSize(QSize(111, 0))
        self.pushButton_17.setMaximumSize(QSize(80, 56))
        self.pushButton_17.setCheckable(False)
        self.pushButton_17.setChecked(False)
        self.pushButton_17.setAutoDefault(False)
        self.pushButton_17.setFlat(False)

        self.verticalLayout_2.addWidget(self.pushButton_17)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMaximumSize(QSize(111, 56))
        self.pushButton_4.setAutoDefault(False)

        self.verticalLayout_2.addWidget(self.pushButton_4)

        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(111, 0))
        self.pushButton_6.setMaximumSize(QSize(80, 56))
        self.pushButton_6.setCheckable(True)
        self.pushButton_6.setChecked(False)

        self.verticalLayout_2.addWidget(self.pushButton_6)

        self.pushButton_20 = QPushButton(self.centralwidget)
        self.pushButton_20.setObjectName(u"pushButton_20")
        self.pushButton_20.setMinimumSize(QSize(111, 0))
        self.pushButton_20.setMaximumSize(QSize(111, 56))

        self.verticalLayout_2.addWidget(self.pushButton_20)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 3, 5, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.toolButton_15 = QToolButton(self.centralwidget)
        self.toolButton_15.setObjectName(u"toolButton_15")
        self.toolButton_15.setMaximumSize(QSize(58, 40))
        self.toolButton_15.setIcon(icon)

        self.horizontalLayout_8.addWidget(self.toolButton_15)

        self.toolButton_16 = QToolButton(self.centralwidget)
        self.toolButton_16.setObjectName(u"toolButton_16")
        self.toolButton_16.setMaximumSize(QSize(58, 40))
        self.toolButton_16.setIcon(icon1)

        self.horizontalLayout_8.addWidget(self.toolButton_16)


        self.gridLayout_2.addLayout(self.horizontalLayout_8, 2, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 729, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuMap = QMenu(self.menubar)
        self.menuMap.setObjectName(u"menuMap")
        self.menuLED = QMenu(self.menubar)
        self.menuLED.setObjectName(u"menuLED")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuMap.menuAction())
        self.menubar.addAction(self.menuLED.menuAction())
        self.menuFile.addAction(self.actionOpen_Project_Folder)
        self.menuFile.addAction(self.actionOpen_HOF)
        self.menuFile.addAction(self.actionSave_to_DB)
        self.menuFile.addAction(self.actionExport_HOF)
        self.menuFile.addAction(self.actionExport_HOF_v2)
        self.menuMap.addAction(self.actionOpen_TTL_for_Route)
        self.menuMap.addAction(self.actionOpen_global_cfg)
        self.menuLED.addAction(self.actionGenerate_8w_6w_LCD)
        self.menuLED.addAction(self.actionGenerate_DPIPv2)
        self.menuEdit.addAction(self.actionPreferences)
        self.menuEdit.addAction(self.actionImport_Busstops_from_list)
        self.menuEdit.addAction(self.actionEric_Guesser)
        self.menuEdit.addAction(self.actionReset_Busstop_List_IDs)
        self.menuEdit.addAction(self.actionEdit_En_Masse)

        self.retranslateUi(MainWindow)

        self.pushButton_17.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"HOF View", None))
        self.actionOpen_Project_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Database", None))
        self.actionOpen_HOF.setText(QCoreApplication.translate("MainWindow", u"Open HOF", None))
        self.actionOpen_TTL_for_Route.setText(QCoreApplication.translate("MainWindow", u"Open TTL for Route", None))
        self.actionSave_to_DB.setText(QCoreApplication.translate("MainWindow", u"Save to DB", None))
        self.actionOpen_global_cfg.setText(QCoreApplication.translate("MainWindow", u"Open global.cfg", None))
        self.actionExport_HOF.setText(QCoreApplication.translate("MainWindow", u"Export HOF", None))
        self.actionGenerate_8w_6w_LCD.setText(QCoreApplication.translate("MainWindow", u"Generate 8w,6w", None))
        self.actionGenerate_DPIPv2.setText(QCoreApplication.translate("MainWindow", u"Generate DPIPv2", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.actionImport_Busstops_from_list.setText(QCoreApplication.translate("MainWindow", u"Import Busstops from list", None))
        self.actionEric_Guesser.setText(QCoreApplication.translate("MainWindow", u"Eric Guesser", None))
        self.actionExport_HOF_v2.setText(QCoreApplication.translate("MainWindow", u"Export HOF v2", None))
#if QT_CONFIG(whatsthis)
        self.actionExport_HOF_v2.setWhatsThis(QCoreApplication.translate("MainWindow", u"A smaller HOF File. Hopefully.", None))
#endif // QT_CONFIG(whatsthis)
        self.actionReset_Busstop_List_IDs.setText(QCoreApplication.translate("MainWindow", u"Reset Busstop List IDs", None))
        self.actionEdit_En_Masse.setText(QCoreApplication.translate("MainWindow", u"Edit En Masse", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Termini", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"Duplicate", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Bus Stops", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"Duplicate", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Duplicate", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"DDU", None))
        self.pushButton_22.setText(QCoreApplication.translate("MainWindow", u"S\n"
"o\n"
"r\n"
"t", None))
#if QT_CONFIG(tooltip)
        self.listWidget_3.setToolTip(QCoreApplication.translate("MainWindow", u"Search...", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.listWidget_3.setStatusTip(QCoreApplication.translate("MainWindow", u"Search...", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.listWidget_3.setWhatsThis(QCoreApplication.translate("MainWindow", u"Search...", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.pushButton_23.setText(QCoreApplication.translate("MainWindow", u"S\n"
"o\n"
"r\n"
"t", None))
        self.pushButton_21.setText(QCoreApplication.translate("MainWindow", u"S\n"
"o\n"
"r\n"
"t", None))
        self.toolButton_5.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_6.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_7.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_8.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Routes", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Duplicate", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Bus Stops", None))
        self.pushButton_24.setText(QCoreApplication.translate("MainWindow", u"Check All\n"
"Busstop Validity", None))
        self.pushButton_18.setText(QCoreApplication.translate("MainWindow", u"Check\n"
"Busstop Validity", None))
#if QT_CONFIG(tooltip)
        self.checkBox.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If checked, will use append mode. Otherwise, insert mode.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Append | Insert", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.pushButton_19.setText(QCoreApplication.translate("MainWindow", u"Check Rt\n"
"Validity", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.toolButton_4.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_3.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"Duplicate\n"
"Without\n"
"Autoskip", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Add from\n"
"selected\n"
"Bus Stop", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Remove\n"
"Selected\n"
"Bus Stop", None))
        self.pushButton_20.setText(QCoreApplication.translate("MainWindow", u"Change\n"
"Current to\n"
"Selected BS", None))
        self.toolButton_15.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.toolButton_16.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuMap.setTitle(QCoreApplication.translate("MainWindow", u"Map", None))
        self.menuLED.setTitle(QCoreApplication.translate("MainWindow", u"LED", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

