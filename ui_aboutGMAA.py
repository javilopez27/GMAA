# Form implementation generated from reading ui file 'c:\Users\00jav\Downloads\GMAA (PyQt6)\aboutGMAA.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AboutGMAA(object):
    def setupUi(self, AboutGMAA):
        AboutGMAA.setObjectName("AboutGMAA")
        AboutGMAA.resize(736, 762)
        AboutGMAA.setStyleSheet("background: #EFEAE6")
        self.centralwidget = QtWidgets.QWidget(parent=AboutGMAA)
        self.centralwidget.setObjectName("centralwidget")
        self.botonOk = QtWidgets.QPushButton(parent=self.centralwidget)
        self.botonOk.setGeometry(QtCore.QRect(320, 630, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setBold(True)
        font.setWeight(75)
        self.botonOk.setFont(font)
        self.botonOk.setObjectName("botonOk")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 30, 321, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(320, 580, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(280, 600, 241, 16))
        self.label_4.setObjectName("label_4")
        self.imagenHelp = QtWidgets.QLabel(parent=self.centralwidget)
        self.imagenHelp.setGeometry(QtCore.QRect(100, 70, 541, 491))
        self.imagenHelp.setText("")
        self.imagenHelp.setPixmap(QtGui.QPixmap("c:\\Users\\00jav\\Downloads\\GMAA (PyQt6)\\images/DIATFG.png"))
        self.imagenHelp.setScaledContents(True)
        self.imagenHelp.setObjectName("imagenHelp")
        AboutGMAA.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=AboutGMAA)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 736, 26))
        self.menubar.setObjectName("menubar")
        AboutGMAA.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=AboutGMAA)
        self.statusbar.setObjectName("statusbar")
        AboutGMAA.setStatusBar(self.statusbar)

        self.retranslateUi(AboutGMAA)
        QtCore.QMetaObject.connectSlotsByName(AboutGMAA)

    def retranslateUi(self, AboutGMAA):
        _translate = QtCore.QCoreApplication.translate
        AboutGMAA.setWindowTitle(_translate("AboutGMAA", "About GMAA"))
        self.botonOk.setText(_translate("AboutGMAA", "OK"))
        self.label_2.setText(_translate("AboutGMAA", "<html>\n"
"  <head/>\n"
"  <body>\n"
"    <p>\n"
"      <span style=\"font-size:12pt; font-family: Open Sans;\">Generic Multi-Attribute Analysis (GMAA)</span>\n"
"    </p>\n"
"  </body>\n"
"</html>"))
        self.label_3.setText(_translate("AboutGMAA", "<html><head/><body><p><span style=\" font-family:\'Open Sans 53\'; font-size:8pt;\">Versión 2.0</span> (2023)</p></body></html>"))
        self.label_4.setText(_translate("AboutGMAA", "<html>\n"
"  <head/>\n"
"  <body>\n"
"    <p>\n"
"      <span style=\"font-size:8pt; font-family: Open Sans Light;\">Web Site http://dia.fi.upm.es/XXX</span>\n"
"    </p>\n"
"  </body>\n"
"</html>"))
