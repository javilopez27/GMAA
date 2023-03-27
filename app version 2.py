import sys
from PyQt6.QtWidgets import QApplication,QGridLayout,QInputDialog, QGraphicsView,QScrollArea, QGraphicsView, QFrame, QWidget,QToolBar, QMainWindow, QFileDialog, QLabel, QMenu, QPushButton, QVBoxLayout, QStatusBar, QHBoxLayout, QLineEdit, QMessageBox
from PyQt6.QtGui import QIcon, QFont, QCursor, QAction, QShortcut, QKeySequence, QColor, QPalette, QPainter, QMouseEvent, QPixmap
from PyQt6.QtCore import QTimer, Qt, QPoint, QUrl, QSize, QPoint,QEvent, pyqtSignal, pyqtSlot
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6 import uic
from ui_aboutGMAA import Ui_AboutGMAA
from ui_guiGMAA import Ui_MainWindow
from ui_LogIn import Ui_LogIn
from ui_nodeInformation import Ui_MainWindow
import networkx as nx # With this library we can save and import any proyect thanks to XML
import xml.etree.ElementTree as ET # XML serialisation library to convert the data structure to an XML file
import os 
import math

PrimaryObjective = False
Branch = 0
Leaf = 0
identifier_labels = 0
currentRow = 0
currentColumn = 0

root = ET.Element("QLabels")

class MyWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    

class VentanaPrincipalGMAA(QMainWindow):

    # signals
    # textChanged = pyqtSignal(str)

    def __init__(self):
        super(VentanaPrincipalGMAA, self).__init__()
        uic.loadUi("guiGMAA.ui", self)
        # carga el icono desde un archivo de imagen
        icono = QIcon("iconoUPM.ico")
        super(VentanaPrincipalGMAA, self).setWindowIcon(
            icono)  # establece el icono de la ventana
        super(VentanaPrincipalGMAA, self).setWindowTitle(
            "GMAA (Generic Multi-Attribute Analysis)")
        super(VentanaPrincipalGMAA, self).statusBar(
        ).showMessage("Current WorkSpace: ")


        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.central_widget = MyWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.central_widget)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.setCentralWidget(self.scroll_area)


        # self.botonDesactivar = self.findChild(QPushButton, "botonDesactivar")

        #Initial Options

        self.InitLabel1 = InitialOptionLabels("New Project")
        self.InitLabel1.setObjectName("New Project")
        # self.InitLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.InitLabel2 = InitialOptionLabels("Open Project")
        self.InitLabel2.setObjectName("Open Project")
        # self.InitLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.UPMLogoInit = QLabel()
        pixmap = QPixmap("images/LOGOTIPO leyenda color PNG.png")
        scaled_pixmap = pixmap.scaled(self.UPMLogoInit.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.UPMLogoInit.setPixmap(scaled_pixmap)
        self.layout.addWidget(self.UPMLogoInit,0,0)
        self.layout.addWidget(self.InitLabel1,1,0)
        self.layout.addWidget(self.InitLabel2,2,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet("background-color: #66CAFE")
        self.menubar.setStyleSheet("background-color: #F0F0F0")
        self.menuWindow.setStyleSheet("background-color: #F0F0F0")
        self.toolBarWGMAA.setStyleSheet("background-color: #F0F0F0")
        self.statusBar.setStyleSheet("background-color: #F0F0F0")
        

        # Labels created
        self.labels = []

        # Saves the previous value in the Save QInputDialog 
        self.previous_value = None

        # Context Menu Creation
        self.context_menuPO = QMenu(self)

        # Enable context menu in the main widget
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menuPO)

        # Initial Menu Buttons
        self.InitLabel1.clicked.connect(self.remove_initial)
        self.InitLabel2.clicked.connect(self.open_workspace2)

        # Action to create the PrimaryObjective Label
        self.actionCPO = QAction("Create a Primary Objective", self)
        # create_PO function to create the PO first Label
        self.actionCPO.triggered.connect(self.create_PO)

        # Action to create the Brach/Leaf Labels
        self.actionCBL = QAction("Create Branches/Leaf", self)
        self.actionCBL.triggered.connect(self.create_BL)

        # Action to delete the Primary Objective Label
        self.actionDPO = QAction("Delete Primary Objective", self)
        self.actionDPO.triggered.connect(self.delete_PO)

        # Adding actions to de the Context Menu Created
        self.context_menuPO.addAction(self.actionCPO)


        # connect Menu signals
        self.actionCredits.triggered.connect(self.fn_help)
        self.actionLogOut.triggered.connect(self.fn_login)
        self.actionNew_Workspace.triggered.connect(self.new_workspace)
        self.actionOpen_Workspace.triggered.connect(self.open_workspace)
        self.actionSave_WorkSpace.triggered.connect(self.save_proInput)
        self.actionSave_WorkSpace_As.triggered.connect(self.save_proInput)
        self.actionClose_WorkSpace.triggered.connect(self.close_workspace)


        # connect Toolbar signals
        self.actionNewWorkspace.triggered.connect(self.new_workspace)
        self.actionExistingWorkspace.triggered.connect(self.open_workspace)
        self.actionSaveWorkspace.triggered.connect(self.save_proInput)
        self.actionLightBulb.triggered.connect(self.fn_help)
        # self.actionPrinter.triggered.connect(self.print_workspace)
        

        # Inhabilitamos todos los botones hasta que no se cree o importe un WorkSpace
        
        self.actionSaveWorkspace.setObjectName("actionSaveWorkspace")
        self.actionViewComponentUtilities.setEnabled(False)
        self.actionAltConsequences.setEnabled(False)
        self.actionAltClassification.setEnabled(False)
        self.actionWeightStabilityIntervals.setEnabled(False)
        self.actionDPOptimality.setEnabled(False)
        self.actionSimulatorTechniques.setEnabled(False)
        self.actionPrinter.setEnabled(False)
        if len(self.labels) == 0: 
            self.actionSaveWorkspace.setEnabled(False)
            self.actionSave_WorkSpace.setEnabled(False)
            self.actionSave_WorkSpace_As.setEnabled(False)
        else: 
            self.actionSaveWorkspace.setEnabled(True)
            self.actionSave_WorkSpace.setEnabled(True)
            self.actionSave_WorkSpace_As.setEnabled(True)
            

        
        # self.textEdit.textChanged.connect(self.fn_toolbarSave) # Si se escribe texto el icono printer se habilita

        # Exit Button
        self.actionExit.triggered.connect(self.close_window)

    # def fn_toolbarSave(self):
    #     if self.textEdit.toPlainText():
    #         self.actionPrinter.setEnabled(True)

    #     else:
    #         self.actionPrinter.setEnabled(False)

    def fn_help(self):
        vHelp = VentanaHelp(self)
        vHelp.show()

    def fn_login(self):
        vLogin = VentanaLogIn(self)
        vLogin.show()

    # removes all the items in the initial screen

    def remove_initial(self):
        self.UPMLogoInit.deleteLater()
        self.InitLabel1.deleteLater()
        self.InitLabel2.deleteLater()
        self.setStyleSheet("background-color: ")
        self.menubar.setStyleSheet("background-color: ")
        self.menuWindow.setStyleSheet("background-color: ")
        self.toolBarWGMAA.setStyleSheet("background-color: ")
        self.statusBar.setStyleSheet("background-color: ")
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.central_widget = MyWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.central_widget)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.setCentralWidget(self.scroll_area)
    
    def new_workspace(self):
        try:    
            label_name = self.InitLabel1.objectName()
            label_name2 = self.InitLabel2.objectName()
            label = self.findChild(QPushButton,label_name)
            label2 = self.findChild(QPushButton,label_name2)
            # labelPixmap = self.findChild(QLabel)
            
            print(f"P: QPushButton Text: {label_name}")
            if label and label2:
                label.deleteLater()
                label2.deleteLater()

            for label in self.findChildren(QLabel):
                if label.pixmap():
                    label.deleteLater()
                    self.setStyleSheet("background-color: ")
                    self.menubar.setStyleSheet("background-color: ")
                    self.menuWindow.setStyleSheet("background-color: ")
                    self.toolBarWGMAA.setStyleSheet("background-color: ")
                    self.statusBar.setStyleSheet("background-color: ")
                    self.scroll_area = QScrollArea(self)
                    self.scroll_area.setWidgetResizable(True)
                    self.central_widget = MyWidget(self)
                    self.setCentralWidget(self.central_widget)
                    self.layout = QGridLayout()
                    self.central_widget.setLayout(self.layout)
                    self.scroll_area.setWidget(self.central_widget)
                    self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
                    self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

                    self.setCentralWidget(self.scroll_area)
        except: 
            pass


    def open_workspace(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo XML", "", "Archivos XML (*.xml)")
        if file_name:
            # Process the XML file here
            print("Archivo seleccionado:", file_name)
            

    def open_workspace2(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo XML", "", "Archivos XML (*.xml)")
        if file_name:
            # Process the XML file here
            print(f"P: Archivo seleccionado: {file_name}")
            self.UPMLogoInit.deleteLater()
            self.InitLabel1.deleteLater()
            self.InitLabel2.deleteLater()
            self.setStyleSheet("background-color: ")
            self.menubar.setStyleSheet("background-color: ")
            self.menuWindow.setStyleSheet("background-color: ")
            self.toolBarWGMAA.setStyleSheet("background-color: ")
            self.statusBar.setStyleSheet("background-color: ")
            self.scroll_area = QScrollArea(self)
            self.scroll_area.setWidgetResizable(True)
            self.central_widget = MyWidget(self)
            self.setCentralWidget(self.central_widget)
            self.layout = QGridLayout()
            self.central_widget.setLayout(self.layout)
            self.scroll_area.setWidget(self.central_widget)

            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

            self.setCentralWidget(self.scroll_area)      



    def save_proInput(self): 
        
        default_value = self.previous_value if self.previous_value is not None else ''
        file_name, ok = QInputDialog.getText(self, "Save Project", "Insert name's project:",text=default_value)
        valueF = file_name
        file_name = file_name + ".xml"   # adds the XML extension
        if ok:  # ok is a boolean that indicates whether the user pressed any optional button.
            self.previous_value = valueF
            self.save_project(file_name)


    def save_project(self, file_path):
        root = ET.Element("Project_GMAA")
        for label in self.labels:
            print("P: Label_name "+str(label.label_name))
            root.append(label.to_xml())

        tree = ET.ElementTree(root)
        tree.write(file_path)


    # What this function does is to ask you what you want to do when you save your workspace 

    def close_workspace(self,event):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf

        if self.labels:
            reply = QMessageBox.question(self, 'Save Changes?', 'Do you want to save changes before closing?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Cancel:
                pass
            elif reply == QMessageBox.StandardButton.Yes:
                self.save_proInput()
            else:
                PrimaryObjective = False
                for label in self.labels:
                    label.deleteLater()
                self.labels = []
                identifier_labels = 0
                PrimaryObjective = False
                Branch = 0           
                Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
                identifier_labels = 0
                currentRow = 0 
                currentColumn = 0
                self.actionSaveWorkspace.setEnabled(False)
                self.actionSave_WorkSpace.setEnabled(False)
                self.actionSave_WorkSpace_As.setEnabled(False)

        else:
            pass
            

    # def print_workspace(self):
    #     printer =  QPrinter(QPrinter.PrinterMode.HighResolution)
    #     dialog = QPrintDialog(printer)

    #     if dialog.exec() == QPrintDialog.DialogCode.Accepted:
    #         self.textEdit.print(printer)

    # Function that shows the Context Menu created before

    def show_context_menuPO(self, point):
        # Show the Context Menu depending on the value of PrimaryObjective
        if self.labels:
            self.context_menuPO.removeAction(self.actionCPO)
            # Adding the Action of creating branches and leaves
            self.context_menuPO.addAction(self.actionCBL)
            # Adding the Action of creating branches and leaves
            self.context_menuPO.addSeparator()
            self.context_menuPO.addAction(self.actionDPO)
        elif not self.labels:
            self.context_menuPO.addAction(self.actionCPO)
            self.context_menuPO.removeAction(self.actionCBL)
            self.context_menuPO.removeAction(self.actionDPO)
        self.context_menuPO.exec(self.mapToGlobal(point))

    def create_PO(self):

        global Leaf
        global identifier_labels
        global PrimaryObjective
        global currentColumn
        PrimaryObjective = True

        
        labelPO = LabelNode(identifier = identifier_labels, text="Ov. Objective",label_name= f"Ov.Objective/PO Label{identifier_labels}",posArray=0,cRow=2,cColumn=0)
        identifier_labels += 1
        self.labels.append(labelPO) # adds PO Label to the list of mainwindow labels
        
        print("P: Number of Labels: "+str(len(self.labels)))
        self.actionSaveWorkspace.setEnabled(True)
        self.actionSave_WorkSpace.setEnabled(True)
        self.actionSave_WorkSpace_As.setEnabled(True)
        print("P: Nodes Identifier is "+str(labelPO.identifier))
        # print("P: "+str(self.labels[identifier_labels-1].label_name))
        Leaf = Leaf + 1
        labelPO.setVisible(True)
        labelPO.setFixedSize(120, 40)
        self.layout.addWidget(labelPO,2,0)
        currentColumn+=1
        
        

        # self.setCentralWidget(labelPO)
        # labelPO.move(200, 100)
        # labelPO.double_clicked.connect(lambda: self.open_NodeInfo(labelPO.identifier))
        labelPO.double_clicked.connect(self.open_NodeInfo)
        
        # XML with ElementTree so that we can save it

    
    def open_NodeInfo(self):
        sender = self.sender()  # Collects all the information of the label that has emitted the double-click signal
        vNodeInfo = VentanaNodeInfo(self)
        # vNodeInfo.textDescription.setPlaceholderText("Enter your node description here...")
        vNodeInfo.textDescription.setPlainText(f"Número de hijos: {len(sender.connections)}.\nConexiones: {sender.connections}") # Test to check posArray from the labels
        vNodeInfo.textUnits.setPlaceholderText("Enter your node units...")
        vNodeInfo.textMinRange.setPlaceholderText("ej. 1")
        vNodeInfo.textMaxRange.setPlaceholderText("ej. 5")
        vNodeInfo.textName.setPlainText(sender.label_name)
        vNodeInfo.textLabel.setPlainText(sender.text())
        
        def copy_text():
            if len(vNodeInfo.textLabel.toPlainText()) > 15:
                QMessageBox.warning(self, "Warning", f"The text cannot exceed 15 characters. There are {len(vNodeInfo.textLabel.toPlainText())} characters.")
                return
            textNameNI = vNodeInfo.textName.toPlainText()
            textLabelNI = vNodeInfo.textLabel.toPlainText()[:15]
            sender.setText(textLabelNI)
            sender.label_name = textNameNI
            vNodeInfo.close()
        
        def enable_apply():
            vNodeInfo.buttonApply.setEnabled(True)
        
        vNodeInfo.textDescription.textChanged.connect(enable_apply)
        vNodeInfo.textLabel.textChanged.connect(enable_apply)
        vNodeInfo.textUnits.textChanged.connect(enable_apply)
        vNodeInfo.textMinRange.textChanged.connect(enable_apply)
        vNodeInfo.textMaxRange.textChanged.connect(enable_apply)
        vNodeInfo.textName.textChanged.connect(enable_apply)
        vNodeInfo.buttonApply.clicked.connect(copy_text)
        vNodeInfo.show()

    # Functions to review

    def create_BL(self):
        global Leaf
        global Branch
        global identifier_labels
        global PrimaryObjective
        global currentColumn
        global currentRow   
        PrimaryObjective = True

        labelLE = LabelNode(identifier= identifier_labels,text="Label"+str(identifier_labels),label_name= "Label"+str(identifier_labels),posArray=len(self.labels))
        identifier_labels+=1
        self.labels.append(labelLE)
        # self.layout.getItemPosition(self.layout.indexOf(self.labels[identifier_labels-2]))
        print("P: Number of Labels: "+str(len(self.labels)))
        print("P: Nodes Identifier is "+str(labelLE.identifier))
        Leaf = Leaf + 1
        labelLE.setVisible(True)
        labelLE.setFixedSize(120, 40)
        if len(self.labels) == 1:
            self.layout.addWidget(labelLE,currentRow,1)
        else: 
            self.layout.addWidget(labelLE,currentRow,currentColumn)
        currentRow+=1
        Branch+=1
        print("P: Number of Labels: "+str(len(self.labels)))
        labelLE.double_clicked.connect(self.open_NodeInfo)

        central_pos = math.floor(currentRow/2)
        self.layout.addWidget(self.labels[0], central_pos-1, 0)
        self.layout.update()

            

        print(f"P: central pos: {central_pos}")

        

    def delete_PO(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf

        for child in self.labels: 
                child.deleteLater()
        self.labels.clear()
        PrimaryObjective = False
        Branch = 0           
        Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
        identifier_labels = 0
        currentRow = 0 
        currentColumn = 0
        
        

    def closeEvent(self,event):
        if self.labels != 0:
            reply = QMessageBox.warning(self, "GMAA WorkSpace", "The WorkSpace Document has been modified. \n Do you want to save changes?", QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Save)

            if reply == QMessageBox.StandardButton.Discard:
                event.accept()

            if reply == QMessageBox.StandardButton.Save:
                event.ignore()
                self.save_workspace()
                self.close_window()

            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()

        else:
            event.accept()

    def close_window(self):
        self.close()  # Cerrar el programa


class VentanaHelp(QMainWindow):

    def __init__(self, parent=None):
        super(VentanaHelp, self).__init__(parent)
        uic.loadUi("aboutGMAA.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaHelp, self).setWindowIcon(icono)
        super(VentanaHelp, self).setWindowTitle("About GMAA")

        self.botonOk.clicked.connect(self.close_windowH)

    def close_windowH(self):
        self.close()


class VentanaLogIn(QMainWindow):

    def __init__(self, parent=None):
        super(VentanaLogIn, self).__init__(parent)
        uic.loadUi("LogIn.ui", self)
        # carga el icono desde un archivo de imagen
        icono = QIcon("iconoUPM.ico")
        super(VentanaLogIn, self).setWindowIcon(
            icono)  # establece el icono de la ventana
        super(VentanaLogIn, self).setWindowTitle("Inicio Sesión")
        self.lineUser.setPlaceholderText(" Please enter your username...")
        self.linePw.setPlaceholderText(" Please enter your password...")
        self.lineInstitution.setPlaceholderText("Please enter your Institution...")
        palette = QPalette()
        color = QColor(255, 255, 255)  # Color Blanco
        palette.setColor(QPalette.ColorRole.Text, color)
        self.lineUser.setPalette(palette)
        self.lineInstitution.setPalette(palette)
        self.linePw.setPalette(palette)
        self.linePw.setEchoMode(QLineEdit.EchoMode.Password)
        self.linePw.setEnabled(False)
        self.lineUser.textChanged.connect(self.enablePw)
        self.botonLogIn.clicked.connect(self.checkUserPw)

        # Para saber cuándo podemos escribir en QLineEdit de LinePw

    def enablePw(self, text):
        if self.lineUser.text():
            self.linePw.setEnabled(True)
        else:
            self.linePw.setEnabled(False)
            # self.linePw.setReadOnly(True)
            self.linePw.clear()

    def checkUserPw(self):
        if self.lineUser.text() == '1' and self.linePw.text() == '1':
            main_window_gmaa = VentanaPrincipalGMAA()
            main_window_gmaa.show()
            self.close()


class VentanaNodeInfo(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaNodeInfo, self).__init__(parent)
        uic.loadUi("nodeInformation.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaNodeInfo, self).setWindowIcon(icono)
        super(VentanaNodeInfo, self).setWindowTitle("Node Information")
        self.VentanaPrincipalGMAA = parent
        
        self.max_length = 15    # maximum number of char

        self.buttonCancel.clicked.connect(self.close_windowNI)
        self.textLabel.textChanged.connect(self.update_label)
        self.textUnits.textChanged.connect(self.update_label)
        self.textMinRange.textChanged.connect(self.update_label)
        self.textMaxRange.textChanged.connect(self.update_label)
        self.textName.textChanged.connect(self.update_label)
        self.textDescription.textChanged.connect(self.update_label)
        self.buttonApply.setEnabled(True)
        # self.buttonOk.clicked.connect(lambda: self.ok_button_clicked(self.sender()))

    def update_label(self):
        self.buttonApply.setEnabled(False)
        self.textLabel.toPlainText()
        # self.parent().labels[identifier_labels-1].setText(text)

    # def ok_button_clicked(self,sender):
    #     textLabelNI = self.textLabel.toPlainText()[:15] 
    #     textNameNI = self.textLabel.toPlainText()
    #     sender.label_name.setText(textLabelNI) 
    #     sender.text().setText(textNameNI) 

    # def update_textLabel_text(self):
    #     self.text = self.textLabel.toPlainText()
    #     self.textLabel.setText(self.text)

    def close_windowNI(self):
        self.close()



class LabelNode(QLabel):
    # connect signals
    double_clicked = pyqtSignal()
    _first_created = False

    def __init__(self, identifier, text, label_name,posArray,cRow,cColumn,parent=None):
        super().__init__(text, parent)
        global PrimaryObjective
        PrimaryObjective = True
        # self.parent = self.parent()
        # Mouse Tracking
        self.setMouseTracking(True)
        self.setObjectName("MyLabel")
        self.clicked = False
        self.identifier = identifier
        self.label_name = label_name
        self.posArray = posArray
        # print(f"P: Parent: {parent.parent}")
        self.connections = []  # this are connections between nodes to know which ones are related
        self.finalNode = True # we make sure it is a final node

        #  also have cRow, cColumn and sons so that when a child is created it will be in the next column but in the same row as its ancestor. 
        self.cRow = cRow
        self.cColumn = cColumn
        

        # connections between labels
        self.connections = set()


        if not LabelNode._first_created:
            LabelNode._first_created = True
            self._active = True
        else:
            self._active = False

        self.setGeometry(130, 210, 131, 41)
        self.setMinimumSize(131,41)
        self.setMaximumSize(131,41)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFrameShape(QLabel.Shape.Box)
        self.setFrameShadow(QLabel.Shadow.Sunken)
        if PrimaryObjective == False:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #7CEE69;")
        else:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;")
        self.setText(text)
        # We can name the PO Label
        # self.setObjectName("Primary Objective Label")
        self.show()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
    
    def add_connection(self, label):
            self.connections.add(label)

    def remove_connection(self, label):
        if label in self.connections:
            self.connections.remove(label)
            if len(self.connections) == 0:
                self.finalNode = True
                self.changeStyleSheet()



    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.clicked = True
        self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.clicked:
            self.move(self.mapToParent(event.pos() - self.offset))
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.clicked = False

    def mouseDoubleClickEvent(self,event):
        self.double_clicked.emit()
        # self.textChanged.emit(self.text())

    def showContextMenu(self, pos):
        global Leaf
        global identifier_labels
    
        menu = QMenu()
        if self.identifier == 0:
            action_name = QAction(f"Name: {self.label_name}", self)
            action_label = QAction(f"Label: {self.text()}", self)
            print("P: Number of Leaf now: "+str(Leaf))
            action_createSon = QAction("Create a son", self)

            action_createSon.triggered.connect(self.create_sonPO)
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(self.deleteLabelPO) 
            menu.addAction(action_name)
            menu.addAction(action_label)
            menu.addSeparator()
            menu.addAction(action_createSon)
            menu.addAction(delete_action)
            menu.exec(self.mapToGlobal(pos))
        else: 
            action_name = QAction("Name: "+str(self.text()), self)
            action_label = QAction("Label: "+str(self.label_name), self)
            print("P: Number of Leaf now: "+str(Leaf))
            action_createSon = QAction("Create a son", self)

            action_createSon.triggered.connect(self.create_son)
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(self.deleteLabelSon)
            # stylesheet_action = QAction("Final node")
            # stylesheet_action.triggered.connect(self.changeStyleSheet)
            menu.addAction(action_name)
            menu.addAction(action_label)
            menu.addSeparator()
            menu.addAction(action_createSon)
            menu.addAction(delete_action)
            menu.addSeparator()
            # menu.addAction(stylesheet_action)
            menu.exec(self.mapToGlobal(pos))

    

    def to_xml(self):
        element = ET.Element("MyLabel")
        element.set("text", self.text())
        element.set("x", str(self.pos().x()))
        element.set("y", str(self.pos().y()))
        element.set("width", str(self.size().width()))
        element.set("height", str(self.size().height()))
        element.set("id",str(self.identifier))
        element.set("label_name",self.label_name)
        psArray = str(self.posArray)
        element.set("posArray",psArray)
        return element
    
    # function I need to fix

    def create_sonPO(self):
        global Leaf
        global Branch
        global identifier_labels
        global PrimaryObjective
        global currentColumn
        global currentRow   
        PrimaryObjective = True
        parent = self.parent()
        

        labelLE = LabelNode(identifier= identifier_labels,text="Label"+str(identifier_labels),label_name= "Label"+str(identifier_labels),
                            posArray=len(parent.parent.labels),cRow=currentRow,cColumn=1)
        labelLE.finalNode = True
        labelLE.changeStyleSheet()
        identifier_labels+=1
        parent.parent.labels.append(labelLE)
        # self.layout.getItemPosition(self.layout.indexOf(self.labels[identifier_labels-2]))
        print(f"P: Number of Labels: {len(parent.parent.labels)}")
        print(f"P: Nodes Identifier is {labelLE.identifier}")
        Leaf = Leaf + 1
        labelLE.setVisible(True)
        labelLE.setFixedSize(120, 40)
        
        parent.parent.layout.addWidget(labelLE,currentRow,1)
        currentRow += 15
        currentColumn += 1
        Branch+=1
        sonsPO = parent.parent.labels[0]
        sonsPO.add_connection(labelLE)
        

        print("P: Number of Labels: "+str(len(parent.parent.labels)))
        labelLE.double_clicked.connect(parent.parent.open_NodeInfo)

        central_pos = math.floor(currentRow/2)
        parent.parent.layout.addWidget(parent.parent.labels[0], central_pos-1, 0)
        parent.parent.layout.update()


    def create_son(self):
        global Leaf
        global Branch
        global identifier_labels
        global PrimaryObjective
        global currentColumn
        global currentRow   
        PrimaryObjective = True
        parent = self.parent()

        labelAnc = parent.parent.labels[self.posArray]
        posA = len(labelAnc.connections)

        labelAnc.finalNode = False
        labelAnc.changeStyleSheet()
            
        # place the QLabels according to the number of children of the ancestor node

        if(posA == 0):
            rowS = labelAnc.cRow
        elif(posA == 1):
            rowS = labelAnc.cRow + 1
        elif(posA == 2):
            rowS = labelAnc.cRow + 2 
        elif(posA == 3):
            rowS = labelAnc.cRow + 3 
        elif(posA == 4):
            rowS = labelAnc.cRow + 4
        elif(posA == 5):
            rowS = labelAnc.cRow + 5
        elif(posA == 6):
            rowS = labelAnc.cRow + 6
        elif(posA == 7):
            rowS = labelAnc.cRow + 7 
        elif(posA == 8):
            rowS = labelAnc.cRow + 8
        elif(posA == 9):
            rowS = labelAnc.cRow + 9
        elif(posA == 10):
            rowS = labelAnc.cRow + 10
        elif(posA == 11):
            rowS = labelAnc.cRow + 11
        elif(posA == 12):
            rowS = labelAnc.cRow + 12
        elif(posA == 13):
            rowS = labelAnc.cRow + 13
        elif(posA == 14):
            rowS = labelAnc.cRow + 14
        elif(posA == 15):
            rowS = labelAnc.cRow + 15

        print(f"P: rowS: {rowS}")
        labelLE = LabelNode(identifier= identifier_labels,text="Label"+str(identifier_labels),label_name= "Label"+str(identifier_labels),
                            posArray=len(parent.parent.labels),cRow=rowS,cColumn=labelAnc.cColumn+1)
        labelLE.finalNode = True
        labelLE.changeStyleSheet()
        

        identifier_labels+=1
        # labelLE.posArray = len(parent.parent.labels)
        parent.parent.labels.append(labelLE)
        # self.layout.getItemPosition(self.layout.indexOf(self.labels[identifier_labels-2]))
        print("P: Number of Labels: "+str(len(parent.parent.labels)))
        print(f"P: Nodes Identifier is {labelLE.identifier}")
        Leaf = Leaf + 1
        labelLE.setVisible(True)
        labelLE.setFixedSize(120, 40)
        
        parent.parent.layout.addWidget(labelLE,labelLE.cRow,labelLE.cColumn)
        currentColumn+=1
        
        
        labelAnc.add_connection(labelLE)
        labelAnc = parent.parent.labels[self.posArray]
        print("P: Number of Labels: "+str(len(parent.parent.labels)))
        labelLE.double_clicked.connect(parent.parent.open_NodeInfo)
        print(f"Número de hijos del nodo anterior: {len(labelAnc.connections)}")

        # central_pos = math.floor(Branch/2)
        # parent.parent.layout.addWidget(parent.parent.labels[0], central_pos-1, 0)
        # parent.parent.layout.update()
        print(f"{parent.parent.labels}")

    def deleteLabelPO(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        
        parent = self.parent()
        
        reply = QMessageBox.warning(self.parent(),'Delete Overall Objetive', 'Are you sure you want to delete the Overall Objective? If you delete it, all other elements will be deleted.',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            pass
        elif reply == QMessageBox.StandardButton.Yes:
            for child in parent.children(): 
                if isinstance(child,QLabel):
                    child.deleteLater()
            parent.parent.labels.clear()
            PrimaryObjective = False
            Branch = 0           
            Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
            identifier_labels = 0
            currentRow = 0 
            currentColumn = 0
            parent.parent.actionSaveWorkspace.setEnabled(False)
            parent.parent.actionSave_WorkSpace.setEnabled(False)
            parent.parent.actionSave_WorkSpace_As.setEnabled(False)
        
            print(parent.parent.labels)

    def deleteLabelSon(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        
        parent = self.parent()
        label_remove = parent.findChildren(QLabel,self.objectName())[self.posArray]
        reply = QMessageBox.warning(self.parent(),f'Delete Leaf {label_remove.label_name}', f'Are you sure you want to delete {label_remove.label_name}? If you delete it, all the connected elements to {label_remove.label_name} will be deleted.',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            pass
        else:
            print(f"P: El QLabel a eliminar es: {label_remove.label_name}")
            if len(label_remove.connections) == 0:
                if label_remove is not None:
                    # I do this to delete the connection with the ancestor since deleting the child is not enough
                    for labelRC in parent.parent.labels:
                          # create a copy of the array before iterating over it
                            labelRC.remove_connection(label_remove)
                            
                    parent.parent.labels.pop(self.posArray)
                    label_remove.deleteLater()
                    # parent.parent.labels[self.identifier] = None
                    print(f"P: ID del Label: {self.identifier}")
                    for i in range(self.posArray,len(parent.parent.labels)):
                        parent.parent.labels[i].posArray = i

                    

                    print("P: Accede a len(label_remove.connections) == 0")
                    print(parent.parent.labels)
                    
            else:
                label_remove.remove_label(label_remove)

            
        
    def remove_label(self, label):
        # Buscar todos los QLabel conectados a este QLabel
        for connected_label in set(label.connections):
            
            # Eliminar los QLabel conectados de forma recursiva
            self.remove_label(connected_label)
        
        # Eliminar el QLabel
        parent = self.parent()
        parent.parent.labels.pop(self.posArray)
        for labelRC in parent.parent.labels:
                          # create a copy of the array before iterating over it
                            labelRC.remove_connection(label)
        # self.connections.remove(label)
        label.deleteLater()
        print()
        for i in range(self.posArray,len(parent.parent.labels)):
                    parent.parent.labels[i].posArray = i


    def changeStyleSheet(self):
        print("P:Accedido a cambiar el changeStyleSheet")
        if self.finalNode:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #7CEE69;")
        else:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;")
                
   
    def __repr__(self):
        return f"LabelNode({self.text()})"


class InitialOptionLabels(QPushButton):
    def __init__(self,text):
        super().__init__(text)
        self.setGeometry(130, 210, 101, 21)
        self.setMinimumSize(131,21)
        self.setMaximumSize(131,21)
        self.setText(text)
        self.setStyleSheet(
            "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;")
        self.show()


# Creación de la línea

# line1 = QFrame()
#         line1.setFrameShape(QFrame.Shape.HLine)
#         line1.setFrameShadow(QFrame.Shadow.Sunken)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaLogIn()
    GUI.show()
    sys.exit(app.exec())
