import sys
from PyQt6.QtWidgets import QApplication,QGridLayout,QComboBox,QInputDialog,QGraphicsLineItem,QRadioButton,QAbstractItemView, QGraphicsView,QScrollArea, QGraphicsView, QTableWidgetItem,QFrame, QWidget,QToolBar, QSpacerItem,QMainWindow, QFileDialog, QLabel, QMenu, QPushButton, QVBoxLayout, QStatusBar, QHBoxLayout, QLineEdit, QMessageBox
from PyQt6.QtGui import QBrush,QIcon,QPen, QFont, QCursor, QAction, QShortcut, QKeySequence, QColor, QPalette, QPainter, QMouseEvent, QPixmap
from PyQt6.QtCore import QTimer, Qt, QPoint, QUrl, QSize, QPoint,QEvent, pyqtSignal, pyqtSlot
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6 import uic
from ui_aboutGMAA import Ui_AboutGMAA
from ui_guiGMAA import Ui_MainWindow
from ui_LogIn import Ui_LogIn
from ui_nodeInformation import Ui_MainWindow
from ui_alternativeConsequences import Ui_MainWindow
import networkx as nx # With this library we can save and import any proyect thanks to XML
import xml.etree.ElementTree as ET # XML serialisation library to convert the data structure to an XML file
import os 
import math
import re
import ast # Abstract Syntax Trees
# import json

PrimaryObjective = False
Branch = 0
Leaf = 0
identifier_labels = 0
currentRow = 0
currentColumn = 0
attributes = []
alternatives = []

root = ET.Element("QLabels")

class MyWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setContentsMargins(200, 200, 200, 200)

    

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

        # self.InitLabel1 = InitialOptionLabels("New Project")
        # self.InitLabel1.setObjectName("New Project")
        # self.InitLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        # self.InitLabel2 = InitialOptionLabels("Open Project")
        # self.InitLabel2.setObjectName("Open Project")
        # self.InitLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.UPMLogoInit = QLabel()
        pixmap = QPixmap("images/LOGOTIPO leyenda color PNG.png")
        scaled_pixmap = pixmap.scaled(self.UPMLogoInit.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.UPMLogoInit.setPixmap(scaled_pixmap)
        self.layout.addWidget(self.UPMLogoInit,0,0)
        # self.layout.addWidget(self.InitLabel1,1,0)
        # self.layout.addWidget(self.InitLabel2,2,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet("background-color: #66CAFE")
        self.menubar.setStyleSheet("background-color: #F0F0F0")
        self.menuWindow.setStyleSheet("background-color: #F0F0F0")
        self.toolBarWGMAA.setStyleSheet("background-color: #F0F0F0")
        self.statusBar.setStyleSheet("background-color: #F0F0F0")
        

        # Labels created
        self.labels = []

        # Lines created
        self.lineB = []
        self.lines = []

        # Saves the previous value in the Save QInputDialog 
        self.previous_value = None

        # pressed New Workspace button variable
        self.pressedNW = False


        # Context Menu Creation
        self.context_menuPO = QMenu(self)

        # Enable context menu in the main widget
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menuPO)

        # Initial Menu Buttons
        # self.InitLabel1.clicked.connect(self.remove_initial)
        # self.InitLabel2.clicked.connect(self.open_workspace2)

        # Action to create the PrimaryObjective Label
        self.actionCPO = QAction("Create a Primary Objective", self)
        # create_PO function to create the PO first Label
        self.actionCPO.triggered.connect(self.new_workspace)

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

        # connect View Alternative signals 
        self.actionView_Alt_Consequences.triggered.connect(self.open_AltCon)


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



    def fn_help(self):
        vHelp = VentanaHelp(self)
        vHelp.show()

    def fn_login(self):
        vLogin = VentanaLogIn(self)
        vLogin.show()

    def getFinalAttributes(self, finalNodes):
        global attributes
        attributes = []

        for node in finalNodes:
            if not node.connections:
                attributes.append(node)

    # removes all the items in the initial screen

    def remove_initial(self):
        self.UPMLogoInit.deleteLater()
        # self.InitLabel1.deleteLater()
        # self.InitLabel2.deleteLater()
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
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        try:    
            if self.pressedNW:
                reply = QMessageBox.question(self, 'Save Changes?', 'Do you want to save changes before creating a new workspace?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
                if reply == QMessageBox.StandardButton.Cancel:
                    pass
                elif reply == QMessageBox.StandardButton.Yes:
                    self.save_proInput()
                    for label in self.labels: 
                        label.deleteLater()
                    self.labels.clear()
                    PrimaryObjective = False
                    Branch = 0           
                    Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
                    identifier_labels = 0
                    currentRow = 0 
                    currentColumn = 0
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
            
                    labelPO = LabelNode(identifier = identifier_labels, text="Ov. Objective",label_name= f"Ov.Objective/PO Label{identifier_labels}",posArray=0,cRow=2,cColumn=0)
                    identifier_labels += 1
                    self.labels.append(labelPO) # adds PO Label to the list of mainwindow labels
                    
                    print(F"P: nº labels in self.labels: {len(self.labels)}")
                    self.actionSaveWorkspace.setEnabled(True)
                    self.actionSave_WorkSpace.setEnabled(True)
                    self.actionSave_WorkSpace_As.setEnabled(True)
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

                elif reply == QMessageBox.StandardButton.No:
                    for label in self.labels: 
                        label.deleteLater()
                    self.labels.clear()
                    PrimaryObjective = False
                    Branch = 0           
                    Leaf = 0  # if the delete button of the PO Label is triggered the num of Leaf is 0
                    identifier_labels = 0
                    currentRow = 0 
                    currentColumn = 0
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
            
                    labelPO = LabelNode(identifier = identifier_labels, text="Ov. Objective",label_name= f"Ov.Objective/PO Label{identifier_labels}",posArray=0,cRow=2,cColumn=0)
                    identifier_labels += 1
                    self.labels.append(labelPO) # adds PO Label to the list of mainwindow labels
                    
                    print(F"P: nº labels in self.labels: {len(self.labels)}")
                    self.actionSaveWorkspace.setEnabled(True)
                    self.actionSave_WorkSpace.setEnabled(True)
                    self.actionSave_WorkSpace_As.setEnabled(True)
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

            if not self.labels and not self.pressedNW:
                self.pressedNW = True
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
            
        
                labelPO = LabelNode(identifier = identifier_labels, text="Ov. Objective",label_name= f"Ov.Objective/PO Label{identifier_labels}",posArray=0,cRow=2,cColumn=0)
                identifier_labels += 1
                self.labels.append(labelPO) # adds PO Label to the list of mainwindow labels
                
                print(F"P: nº labels in self.labels: {len(self.labels)}")
                self.actionSaveWorkspace.setEnabled(True)
                self.actionSave_WorkSpace.setEnabled(True)
                self.actionSave_WorkSpace_As.setEnabled(True)
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
        
        except: 
            pass

    def place_lines(self): 

        label_item_connections = 0

        for line in self.lineB:
            try:
                line.deleteLater()
                self.lineB.pop(line)
            except:
                pass

        for line in self.lines:
            try:
                line.deleteLater()
                self.lines.pop(line)

            except:
                pass
            # self.layout.removeWidget(line)
        if not self.labels:
            return

        labelPO = self.labels[0]
        if labelPO is not None and labelPO.connections:
            connection_listPO = labelPO.connections
            for k in range(len(connection_listPO)):
                if k == 0:
                    line = DLineFrameB()
                    self.layout.addWidget(line, 0, 1, 3, 1)
                    line.lower()
                    self.lineB.append(line)
                    print(f"P: DLineFrame {line}")

                else: 
                    numero = k * 15
                    connection = connection_listPO[k]
                    line = DLineFrame(dRow=labelPO.cRow,dColumn=connection.cColumn-1,dNum=numero-1)
                    line.dRow = labelPO.cRow
                    line.dColumn = connection.cColumn-1
                    line.dNum = numero-1
                    self.layout.addWidget(line,line.dRow,line.dColumn,line.dNum,2)
                    line.lower()
                    self.lines.append(line)

        for i in range(1,len(self.labels)):
            label = self.labels[i]

            # label_item = self.layout.itemAtPosition(label.cRow-1,label.cColumn).widget()
            # label_item_connections = len(label_item.connections)
            
            if label.connections:
                for j in range(len(label.connections)):
                    numero = label.cRow
                    resultado = numero % 15
                    for i in range(15, 151, 15):
                        if numero >= i:
                            resultado = numero % i
                    for i in range(resultado):
                        label_item = self.layout.itemAtPosition(label.cRow-i,label.cColumn)
                        
                        if hasattr(label_item,'connections'):
                            label_item = label_item.widget()
                            label_item_connections = len(label_item.connections)
                        else:
                            return
                    

                    numero = label_item_connections 
                    connection_list = label.connections
                    connection = connection_list[j]
                    if label.cRow == connection.cRow:
                        line = HLineFrame()
                        self.layout.addWidget(line,label.cRow,connection.cColumn-1,1,2)
                    else:
                        line = DLineFrame(dRow=label.cRow,dColumn=connection.cColumn-1,dNum=numero+j+1)
                        self.layout.addWidget(line,label.cRow,connection.cColumn-1,numero+j+1,2)
                    line.lower()
                    self.lines.append(line)

        self.layout.update()


    def open_workspace(self):
        global identifier_labels

        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo XML", "", "Archivos XML (*.xml)")
        if file_name:
            # Process the XML file here
            print(f"P: Archivo seleccionado: {file_name}")
            try:
                self.UPMLogoInit.deleteLater()
                # self.InitLabel1.deleteLater()
                # self.InitLabel2.deleteLater()
            except RuntimeError:
                pass
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

            tree = ET.parse(file_name)
            root = tree.getroot()
            for child in root:
                if child.tag == 'MyLabel':
                    cUnitType = child.get('unitType')
                    if cUnitType == "":
                        label = LabelNode(identifier = int(child.get('id')),text = child.get('text'),cRow=int(child.get('cRow')),cColumn=int(child.get('cColumn')),posArray=int(child.get('posArray')),label_name=child.get('label_name'))
                        label.connections = child.get('connections')
                        self.labels.append(label)
                        self.layout.addWidget(label, label.cRow, label.cColumn)
                    elif cUnitType == "Continuous":
                        label = LabelNode(identifier = int(child.get('id')),text = child.get('text'),cRow=int(child.get('cRow')),cColumn=int(child.get('cColumn')),posArray=int(child.get('posArray')),label_name=child.get('label_name'))
                        label.connections = child.get('connections')
                        label.unitType = cUnitType
                        label.unitDescription = child.get('unitDescription')
                        label.unitName = child.get('unitName')
                        label.minRange = int(child.get('minRange'))
                        label.maxRange = int(child.get('maxRange'))
                        self.labels.append(label)
                        self.layout.addWidget(label, label.cRow, label.cColumn)

                    elif cUnitType == "Discrete":
                        label = LabelNode(identifier = int(child.get('id')),text = child.get('text'),cRow=int(child.get('cRow')),cColumn=int(child.get('cColumn')),posArray=int(child.get('posArray')),label_name=child.get('label_name'))
                        label.unitType = cUnitType
                        label.unitDescription = child.get('unitDescription')
                        # label.optionDiscrete = child.get('optionDiscrete')
                        my_var = child.get('optionsList')
                        label.optionsList = ast.literal_eval(my_var)
                        self.labels.append(label)
                        self.layout.addWidget(label, label.cRow, label.cColumn)
                        # print(my_arr)  # ['Option1', 'Option2', 'Option3']


                    
                    
                    
                # elif child.tag == 'dlineframeb':
                #     dlineframeb = DLineFrameB()
                #     self.lineB.append(dlineframeb)
                #     self.layout.addWidget(dlineframeb, 0, 1,3,1)
                # elif child.tag == 'dlineframe':
                #     dRowNumber = int(child.get('row'))
                #     dColumnNumber = int(child.get('column'))
                #     dNumNumber = int(child.get('num'))
                #     dlineframe = DLineFrame(dRow=dRowNumber,dColumn=dColumnNumber,dNum=dNumNumber)
                #     self.lines.append(dlineframe)
                #     self.layout.addWidget(dlineframe, dRowNumber, dColumnNumber,dNumNumber,2)
                #     dlineframe.lower()

            

            # We establish the connections again
            
            for label in self.labels:
                # label_nodes = "[LabelNode(Label2), LabelNode(Label1)]"
                label.double_clicked.connect(self.open_NodeInfo)

                if label.connections:
                    label_names = re.findall(r"LabelNode\((.*?)\)", str(label.connections)) # Exit: ["Label2", "Label1"]
                    label.connections = []
                    for labelC in self.labels:
                        if labelC.text() in label_names:
                            label.connections.append(labelC) 
                
                identifier_labels = len(self.labels)
                # print(f"P: Importar conections: {label.connections}")


            
            self.changeStyleSheetGlobal()
            self.place_lines()
            self.actionSaveWorkspace.setEnabled(True)
            
            file_name = os.path.basename(file_name)
            super(VentanaPrincipalGMAA, self).statusBar().showMessage(f"Current WorkSpace: {file_name}")



    def open_workspace2(self):
        global identifier_labels

        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo XML", "", "Archivos XML (*.xml)")
        if file_name:
            # Process the XML file here
            print(f"P: Archivo seleccionado: {file_name}")
            self.UPMLogoInit.deleteLater()
            # self.InitLabel1.deleteLater()
            # self.InitLabel2.deleteLater()
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
                

            tree = ET.parse(file_name)
            root = tree.getroot()
            for child in root:
                if child.tag == 'MyLabel':
                    label = LabelNode(identifier = int(child.get('id')),text = child.get('text'),cRow=int(child.get('cRow')),cColumn=int(child.get('cColumn')),posArray=int(child.get('posArray')),label_name=child.get('label_name'))
                    label.connections = child.get('connections')
                    self.labels.append(label)
                    self.layout.addWidget(label, label.cRow, label.cColumn)
                # elif child.tag == 'dlineframeb':
                #     dlineframeb = DLineFrameB()
                #     self.lineB.append(dlineframeb)
                #     self.layout.addWidget(dlineframeb, 0, 1,3,1)
                # elif child.tag == 'dlineframe':
                #     dRowNumber = int(child.get('row'))
                #     dColumnNumber = int(child.get('column'))
                #     dNumNumber = int(child.get('num'))
                #     dlineframe = DLineFrame(dRow=dRowNumber,dColumn=dColumnNumber,dNum=dNumNumber)
                #     self.lines.append(dlineframe)
                #     self.layout.addWidget(dlineframe, dRowNumber, dColumnNumber,dNumNumber,2)
                #     dlineframe.lower()

            

            # We establish the connections again
            
            for label in self.labels:
                # label_nodes = "[LabelNode(Label2), LabelNode(Label1)]"
                label.double_clicked.connect(self.open_NodeInfo)

                if label.connections:
                    label_names = re.findall(r"LabelNode\((.*?)\)", str(label.connections)) # Exit: ["Label2", "Label1"]
                    label.connections = []
                    for labelC in self.labels:
                        if labelC.text() in label_names:
                            label.connections.append(labelC) 
                
                identifier_labels = len(self.labels)
                # print(f"P: Importar conections: {label.connections}")



            self.changeStyleSheetGlobal()
            self.place_lines()
            self.actionSaveWorkspace.setEnabled(True)

            file_name = os.path.basename(file_name)
            super(VentanaPrincipalGMAA, self).statusBar().showMessage(f"Current WorkSpace: {file_name}")
    

    def changeStyleSheetGlobal(self):
        for label in self.labels:
            if not label.connections:
                label.finalNode = True
                label.setStyleSheet("background-color: #AAA8A8; border-radius: 6px; border: 1px solid #7CEE69;")
            else: 
                label.finalNode = False
                label.setStyleSheet("background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;")



    def save_proInput(self): 
        # the default_value and self.previous_value variables are used to identify 
        # the value of the previously saved file so that the user does not forget it.
        default_value = self.previous_value if self.previous_value is not None else ''
        file_name, ok = QFileDialog.getSaveFileName(self, 'Save Project', default_value, 'XML files (*.xml)')
        valueF = file_name
        # file_name = file_name  # adds the XML extension
        if ok:  # ok is a boolean that indicates whether the user pressed any optional button.
            self.previous_value = valueF
            self.save_project(file_name)


    def save_project(self, file_path):
        root = ET.Element("Project_GMAA")
        # Loop through the elements of the label array
        for label in self.labels:
            element = ET.Element("MyLabel")
            element.set("text", label.text())
            element.set("cRow", str(label.cRow))
            element.set("cColumn", str(label.cColumn))
            element.set("id",str(label.identifier))
            element.set("label_name",label.label_name)
            element.set("posArray",str(label.posArray))
            element.set("connections",str(label.connections))
            element.set("nodeDescription",label.nodeDescription)

            if label.unitType == "Continuous":
                element.set("unitType","Continuous")
                element.set("unitDescription",label.unitDescription)
                element.set("unitName",label.unitName)
                element.set("minRange",str(label.minRange))
                element.set("maxRange",str(label.maxRange))

            
            elif label.unitType == "Discrete":
                element.set("unitType","Discrete")
                element.set("unitDescription",label.unitDescription)
                # element.set("optionDiscrete",label.optionDiscrete)
                element.set("optionsList",str(label.optionsList))

            else:
                element.set("unitType","")


            root.append(element)
        tree = ET.ElementTree(root)
        tree.write(file_path)

    # connections = []
    # for label1 in self.labels:
    #     for label2 in self.labels:
    #         if label1 is not label2 and label1.text() == label2.text():
    #             if label1 not in connections:
    #                 connections.append(label1)
    #             if label2 not in connections:
    #                 connections.append(label2)



    

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
                print(self.labels)
                for label in self.labels:
                    if label:
                        label.deleteLater()
                self.labels.clear()
                self.lineB.clear()
                self.lines.clear()
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
                self.place_lines()

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

    # def create_PO(self):

    #     global Leaf
    #     global identifier_labels
    #     global PrimaryObjective
    #     global currentColumn
    #     PrimaryObjective = True

        
    #     labelPO = LabelNode(identifier = identifier_labels, text="Ov. Objective",label_name= f"Ov.Objective/PO Label{identifier_labels}",posArray=0,cRow=2,cColumn=0)
    #     identifier_labels += 1
    #     self.labels.append(labelPO) # adds PO Label to the list of mainwindow labels
        
    #     print("P: Number of Labels: "+str(len(self.labels)))
    #     self.actionSaveWorkspace.setEnabled(True)
    #     self.actionSave_WorkSpace.setEnabled(True)
    #     self.actionSave_WorkSpace_As.setEnabled(True)
    #     print("P: Nodes Identifier is "+str(labelPO.identifier))
    #     # print("P: "+str(self.labels[identifier_labels-1].label_name))
    #     Leaf = Leaf + 1
    #     labelPO.setVisible(True)
    #     labelPO.setFixedSize(120, 40)
    #     self.layout.addWidget(labelPO,2,0)
    #     currentColumn+=1
        
        

    #     # self.setCentralWidget(labelPO)
    #     # labelPO.move(200, 100)
    #     # labelPO.double_clicked.connect(lambda: self.open_NodeInfo(labelPO.identifier))
    #     labelPO.double_clicked.connect(self.open_NodeInfo)
        
    #     # XML with ElementTree so that we can save it

    
    
    def open_NodeInfo(self):
        global attributes
        global alternatives
        sender = self.sender()  # Collects all the information of the label that has emitted the double-click signal
        vNodeInfo = VentanaNodeInfo(self)
        # vNodeInfo.textDescription.setPlaceholderText("Enter your node description here...")
        vNodeInfo.textDescription.setPlainText(f"Número de hijos: {len(sender.connections)}.\nConexiones: {sender.connections}. \nUnit type: {sender.unitType}\nTable Discrete: {sender.optionsList}\nFinal Nodes: {attributes}\nAlternatives: {alternatives}\nAttributes: {attributes}") # Test to check posArray from the labels
        # vNodeInfo.textUnits.setPlaceholderText("Enter your node units...")
        # vNodeInfo.textMinRange.setPlaceholderText("ej. 1")
        # vNodeInfo.textMaxRange.setPlaceholderText("ej. 5")
        vNodeInfo.textName.setPlainText(sender.label_name)
        vNodeInfo.textLabel.setPlainText(sender.text())

        # several options if the string is empty, continuous or discrete

        if not sender.unitType:
            vNodeInfo.textDescCont.setPlaceholderText("Enter your node description here...")
            vNodeInfo.textUnitsCont.setPlaceholderText("Enter your node units...")
            vNodeInfo.textMinRangeCont.setPlaceholderText("ej. 1")
            vNodeInfo.textMaxRangeCont.setPlaceholderText("ej. 5")
            vNodeInfo.textDescDisc.setPlaceholderText("Enter your node description here...")
        

        # # tipe of the node

        # self.nodeDescription = ""
        
        # # tipe of the unit

        # self.unitType = ""
        # self.unitDescription = ""
        # self.unitName = ""
        # self.minRange = 0
        # self.maxRange = 1
        # self.optionDiscrete = "" 

        elif sender.unitType == "Continuous":
            vNodeInfo.radioBCont.setChecked(True)
            vNodeInfo.textName.setPlainText(sender.label_name)
            vNodeInfo.textLabel.setPlainText(sender.text())
            vNodeInfo.textUnitsCont.setPlainText(sender.unitName)
            vNodeInfo.textDescCont.setPlainText(sender.unitDescription)
            vNodeInfo.textMinRangeCont.setPlainText(sender.minRange)
            vNodeInfo.textMaxRangeCont.setPlainText(sender.maxRange)

            
        elif sender.unitType == "Discrete":
            vNodeInfo.textDescDisc.setPlainText(sender.unitDescription)
            vNodeInfo.radioBDisc.setChecked(True)
            vNodeInfo.spinBoxDiscrete.setValue(len(sender.optionsList)) 
            # we create the table
            # Adding elements to the table
            num_rows = len(sender.optionsList)
            widthTable = vNodeInfo.tableDiscrete.width()
            vNodeInfo.tableDiscrete.setRowCount(num_rows)
            vNodeInfo.tableDiscrete.setColumnCount(1)
            vNodeInfo.tableDiscrete.setColumnWidth(0, widthTable)
            vNodeInfo.tableDiscrete.setHorizontalHeaderLabels(['Attributes'])
            # vNodeInfo.tableDiscrete.setColumnWidth(0, 190)


            for i in range(num_rows):
                # Add text in the first column
                item = QTableWidgetItem(sender.optionsList[i])
                vNodeInfo.tableDiscrete.setItem(i, 0, item)

                # Add option in second column
                # radio_button = QRadioButton()
                # radio_button.setObjectName(str(i))
                # if item.text() == sender.optionDiscrete:
                #     radio_button.setChecked(True)
                # vNodeInfo.tableDiscrete.setCellWidget(i, 1, radio_button)
                # widget = vNodeInfo.tableDiscrete.cellWidget(i, 1)
                # if isinstance(widget, QRadioButton):
                #     widget.setStyleSheet('margin-left: 10px;')

        vNodeInfo.textLabel.setPlainText(sender.text())
        # vNodeInfo.textLabel.setPlainText(sender.text())

        # create VAC Table

        # establish the alternative for the attribute table

        attributeName = sender.text()
        textMinRange = sender.minRange
        textMaxRange = sender.maxRange
        index = None
        
        for i, attr in enumerate(attributes):
            if attr.unitType == "Continuous":
                if (str(attr.minRange) == textMinRange) and (str(attr.maxRange) == textMaxRange):
                    index = i
                    break
                else:
                    index = None
            elif attr.unitType == "Discrete":
                items = []
                for j in range(vNodeInfo.tableDiscrete.rowCount()):
                    item = vNodeInfo.tableDiscrete.item(j, 0)
                    if item is not None:
                        items.append(item.text())
                if attr.optionsList == items:
                    index = i
                    break
                else:
                    index = None
        
        
        
        num_columns = (len(alternatives) + 1)*2 
        widthTable = vNodeInfo.tableWidgetVAC.width() // 12
        vNodeInfo.tableWidgetVAC.setRowCount(1)
        vNodeInfo.tableWidgetVAC.setColumnCount(num_columns)

        

        # vNodeInfo.tableWidgetAC.setSpan(0, 0, 1, 2) # ocupies two columns
        vNodeInfo.tableWidgetVAC.verticalHeader().setVisible(False)


        for i in range(num_columns):
            vNodeInfo.tableWidgetVAC.setColumnWidth(i, widthTable)
        
        vNodeInfo.tableWidgetVAC.setHorizontalHeaderItem(0, QTableWidgetItem("Attribute"))
        vNodeInfo.tableWidgetVAC.setHorizontalHeaderItem(1, QTableWidgetItem(""))
        item = QTableWidgetItem(attributeName)
        # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        vNodeInfo.tableWidgetVAC.setSpan(0, 0, 1, 2)
        vNodeInfo.tableWidgetVAC.setItem(0, 0, item)

        if not (index == None):
            column = 0
            for alternative in alternatives:
                header_item = QTableWidgetItem(alternative.name)
                vNodeInfo.tableWidgetVAC.setHorizontalHeaderItem(column+2, header_item)
                vNodeInfo.tableWidgetVAC.setHorizontalHeaderItem(column+3, QTableWidgetItem(""))
                print(f"len(alternative.attr): {len(alternative.attr)} index: {index} ")
                elementCD = alternative.attr[index]
                if isinstance(elementCD, ContinuousAttribute):
                    value1 = elementCD.value1
                    value2 = elementCD.value2
                    item = QTableWidgetItem(value1)
                    item2 = QTableWidgetItem(value2)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    vNodeInfo.tableWidgetVAC.setItem(0, column+2, item)
                    item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    vNodeInfo.tableWidgetVAC.setItem(0, column+3, item2)
                elif isinstance(elementCD, DiscreteAttribute):
                    vNodeInfo.tableWidgetVAC.setSpan(0, column+2, 1, 2) 
                    # combo_box = QComboBox()
                    # combo_box.addItems(elementCD.attributenames)
                    selected_option = elementCD.selected
                    # index1 = elementCD.attributenames.index(selected_option)
                    # combo_box.setCurrentIndex(index1)
                    vNodeInfo.tableWidgetVAC.setItem(0, column+2, QTableWidgetItem(selected_option))
                    # vNodeInfo.tableWidgetVAC.setCellWidget(0, column+2, combo_box)
                column+=2
        else:
            pass






        def copy_text():
            if len(vNodeInfo.textLabel.toPlainText()) > 15:
                QMessageBox.warning(self, "Warning", f"The text cannot exceed 15 characters. There are {len(vNodeInfo.textLabel.toPlainText())} characters.")
                return
            textNameNI = vNodeInfo.textName.toPlainText()
            textDescNI = vNodeInfo.textDescription.toPlainText()
            textLabelNI = vNodeInfo.textLabel.toPlainText()[:15]
            sender.setText(textLabelNI)
            sender.label_name = textNameNI
            sender.nodeDescription = textDescNI
            
            if vNodeInfo.radioBCont.isChecked():
                sender.unitType = "Continuous"
                textDC = vNodeInfo.textDescCont.toPlainText()
                sender.unitDescription = textDC
                textUC = vNodeInfo.textUnitsCont.toPlainText()
                sender.unitName = textUC
                textMN = vNodeInfo.textMinRangeCont.toPlainText()
                sender.minRange = textMN
                textMX = vNodeInfo.textMaxRangeCont.toPlainText()
                sender.maxRange = textMX

            

            elif vNodeInfo.radioBDisc.isChecked():
                sender.unitType = "Discrete"
                textDD = vNodeInfo.textDescDisc.toPlainText()
                sender.unitDescription = textDD
                sender.optionsList.clear()
                for i in range(vNodeInfo.tableDiscrete.rowCount()):
                    item = vNodeInfo.tableDiscrete.item(i, 0)
                    if item is not None:
                        sender.optionsList.append(item.text())

                # sender.optionDiscrete = ""
                # for i in range(vNodeInfo.tableDiscrete.rowCount()):
                #     radio_button = vNodeInfo.tableDiscrete.cellWidget(i, 1)
                #     if isinstance(radio_button, QRadioButton) and radio_button.isChecked():
                #         sender.optionDiscrete = vNodeInfo.tableDiscrete.item(i, 0).text()
                #         break



            vNodeInfo.close()
        
        # If one of these widgets change, SAVE button available

        def enable_apply():
            vNodeInfo.buttonApply.setEnabled(True)
        
        vNodeInfo.textDescription.textChanged.connect(enable_apply)
        vNodeInfo.textLabel.textChanged.connect(enable_apply)

        vNodeInfo.textDescCont.textChanged.connect(enable_apply)
        vNodeInfo.textUnitsCont.textChanged.connect(enable_apply)
        vNodeInfo.textMinRangeCont.textChanged.connect(enable_apply)
        vNodeInfo.textMaxRangeCont.textChanged.connect(enable_apply)
        vNodeInfo.textDescDisc.textChanged.connect(enable_apply)
        vNodeInfo.textName.textChanged.connect(enable_apply)
        vNodeInfo.buttonApply.clicked.connect(copy_text)
        vNodeInfo.show()

    def open_AltCon(self):
        self.vAltCon = VentanaAltCon()
        self.vAltCon.show()



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
            reply = QMessageBox.warning(self.parent(), "GMAA WorkSpace", "The WorkSpace Document has been modified. \n Do you want to save changes?", QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Save)

            if reply == QMessageBox.StandardButton.Discard:
                event.accept()

            if reply == QMessageBox.StandardButton.Save:
                event.ignore()
                self.save_proInput()
                self.close_window()

            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()

        else:
            event.accept()

    def close_window(self):
        self.close()  # Cerrar el programa

# window to help the user

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

   # To know when we can write in LinePw's QLineEdit

    def enablePw(self, text):
        if self.lineUser.text():
            self.linePw.setEnabled(True)
        else:
            self.linePw.setEnabled(False)
            # self.linePw.setReadOnly(True)
            self.linePw.clear()

    # we check the user - password

    def checkUserPw(self):
        if self.lineUser.text() == '1' and self.linePw.text() == '1':
            main_window_gmaa = VentanaPrincipalGMAA()
            main_window_gmaa.show()
            # main_window_gmaa.show()
            self.close()


class VentanaAltCon(QMainWindow):
    global attributes
    def __init__(self,parent=None):
        super(VentanaAltCon, self).__init__(parent)
        uic.loadUi("alternativeConsequences.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaAltCon, self).setWindowIcon(icono)
        super(VentanaAltCon, self).setWindowTitle("Alternative Consequences")
        self.VentanaPrincipalGMAA = parent

        if alternatives:
            self.altName = []
            for obj in alternatives:
                self.altName.append(obj.name)
            
            self.comboBoxANames.addItems(self.altName)

        # button signals
        self.pushButtonAA.clicked.connect(self.open_AddAlt)
        self.pushButtonDA.clicked.connect(self.delete_Alt)
        self.pushButtonOkAC.clicked.connect(self.close)


        self.attName = []
        for obj in attributes:
            self.attName.append(obj.text())

        num_rows = len(attributes)
        num_columns = (len(alternatives) + 1)*2 
        widthTable = self.tableWidgetAC.width() // 12
        self.tableWidgetAC.setRowCount(num_rows)
        self.tableWidgetAC.setColumnCount(num_columns)
        self.tableWidgetAC.setColumnWidth(0, widthTable)
        header_item = QTableWidgetItem("Attributes")
        self.tableWidgetAC.setHorizontalHeaderItem(0, header_item)
        self.tableWidgetAC.setHorizontalHeaderItem(1, QTableWidgetItem(""))

        # self.tableWidgetAC.setSpan(0, 0, 1, 2) # ocupies two columns
        self.tableWidgetAC.verticalHeader().setVisible(False)


        for i in range(num_columns):
            self.tableWidgetAC.setColumnWidth(i, widthTable)

        for i, attribute in enumerate(self.attName):
            item = QTableWidgetItem(attribute)
            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidgetAC.setSpan(i, 0, 1, 2)
            self.tableWidgetAC.setItem(i, 0, item)
        
        column = 0
        for i, altern in enumerate(alternatives):
            header_item = QTableWidgetItem(altern.name)
            self.tableWidgetAC.setHorizontalHeaderItem(column+2, header_item)
            self.tableWidgetAC.setHorizontalHeaderItem(column+3, QTableWidgetItem(""))
            # self.tableWidgetAC.setSpan(i, 0, 1, 2)
            for j, elem in enumerate(altern.attr):
                # optionCD = altern.attr[j]
                if isinstance(elem, ContinuousAttribute):
                    value1 = elem.value1
                    value2 = elem.value2
                    item = QTableWidgetItem(value1)
                    item2 = QTableWidgetItem(value2)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tableWidgetAC.setItem(j, column+2, item)
                    item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.tableWidgetAC.setItem(j, column+3, item2)
                elif isinstance(elem, DiscreteAttribute):
                    self.tableWidgetAC.setSpan(j, column+2, 1, 2) 
                    # combo_box = QComboBox()
                    # combo_box.addItems(elem.attributenames)
                    selected_option = elem.selected
                    # index = elem.attributenames.index(selected_option)
                    # combo_box.setCurrentIndex(index)
                    # self.tableWidgetAC.setCellWidget(j, column+2, combo_box)
                    self.tableWidgetAC.setItem(j, column+2, QTableWidgetItem(selected_option))
            column += 2 



    def delete_Alt(self):
        current_value = self.comboBoxANames.currentText()
        reply = QMessageBox.question(self ,'Confirmation', f'Surely you want to delete the alternative {current_value}?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            for altern in alternatives:
                if altern.name == current_value:
                    alternatives.remove(altern)
                    del altern
            
            self.vAltCon = VentanaAltCon()
            self.vAltCon.show()
            self.close()

        else:
            pass

    
    def open_AddAlt(self):
        self.vAddAlt = VentanaAddAlt()
        self.vAddAlt.show()
        self.close()



class VentanaAddAlt(QMainWindow):
    def __init__(self,parent=None):
        global attributes 
        super(VentanaAddAlt, self).__init__(parent)
        uic.loadUi("addAlternative.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaAddAlt, self).setWindowIcon(icono)
        super(VentanaAddAlt, self).setWindowTitle("Add Alternative")

        # buttons signals
        self.pushButtonCancelar.clicked.connect(self.closeW)
        self.pushButtonOk.clicked.connect(self.addAlternativeOption)

        # connect the three table's ScrollBars
        self.tableWidgetAttributesNames.verticalScrollBar().valueChanged.connect(
            self.tableWidgetAA.verticalScrollBar().setValue)
        
        self.tableWidgetAttributesNames.verticalScrollBar().valueChanged.connect(
            self.tableWidgetMinMax.verticalScrollBar().setValue)
        
        self.tableWidgetAA.verticalScrollBar().valueChanged.connect(
            self.tableWidgetAttributesNames.verticalScrollBar().setValue)
        
        self.tableWidgetAA.verticalScrollBar().valueChanged.connect(
            self.tableWidgetMinMax.verticalScrollBar().setValue)
        
        self.tableWidgetMinMax.verticalScrollBar().valueChanged.connect(
            self.tableWidgetAttributesNames.verticalScrollBar().setValue)
        
        self.tableWidgetMinMax.verticalScrollBar().valueChanged.connect(
            self.tableWidgetAA.verticalScrollBar().setValue)


        


        self.attName = []
        for obj in attributes:
            try:
                self.attName.append(obj.text())
            except RuntimeError as e:
                print("Ocurrió un error al obtener el texto del objeto:", e)

        self.attCD = []
        for attr in attributes:
            if attr.unitType == 'Continuous':
                continuous_attr = ContinuousAttribute(attr.minRange,attr.maxRange)
                self.attCD.append(continuous_attr)
            elif attr.unitType == 'Discrete':
                discrete_attr = DiscreteAttribute(attr.optionsList)
                self.attCD.append(discrete_attr)
            else:
                # Si el valor de unitType no es ni 'Continuous' ni 'Discrete'
                # hacer algo aquí en consecuencia
                pass

        

        num_rows = len(attributes)
        widthTable = self.tableWidgetAttributesNames.width()
        self.tableWidgetAttributesNames.setRowCount(num_rows)
        self.tableWidgetAttributesNames.setColumnCount(1)
        self.tableWidgetAttributesNames.setColumnWidth(0, widthTable)

        for i, attribute in enumerate(self.attName):
            item = QTableWidgetItem(attribute)
            # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidgetAttributesNames.setItem(i, 0, item)
        

        widthTable = self.tableWidgetMinMax.width()
        self.tableWidgetMinMax.setRowCount(num_rows)
        self.tableWidgetMinMax.setColumnCount(1)
        self.tableWidgetMinMax.setColumnWidth(0, widthTable)

        for i,attribute in enumerate(self.attCD):
            if isinstance(attribute, ContinuousAttribute):
                item = QTableWidgetItem(" ( " + attribute.value1+ " , " + attribute.value2 + " )")
                self.tableWidgetMinMax.setItem(i, 0, item)
            elif isinstance(attribute, DiscreteAttribute):
                options_str = ", ".join(attribute.attributenames)
                item = QTableWidgetItem(options_str)
                self.tableWidgetMinMax.setItem(i, 0, item)

                
        widthTable = self.tableWidgetAA.width()
        self.tableWidgetAA.setRowCount(num_rows)
        self.tableWidgetAA.setColumnCount(2)
        self.tableWidgetAA.setColumnWidth(0, widthTable//2)
        self.tableWidgetAA.setColumnWidth(1, widthTable//2)

        for i,attribute in enumerate(self.attCD):
            if isinstance(attribute, DiscreteAttribute):
                self.tableWidgetAA.setSpan(i, 0, 1, 2) 
                combo_box = QComboBox()
                combo_box.addItems(attribute.attributenames)
                self.tableWidgetAA.setCellWidget(i, 0, combo_box) 

                
          # tableWidgetAA      
            
        # my_attribute_names = my_array[5].attributenames

        # Creamos un array para guardar los objetos de la clase ContinuousAttribute
    def addAlternativeOption(self):
        global alternatives
        self.alternativeList = []

        # check loop for correct interval values

        for i,attribute in enumerate(self.attCD):
            if isinstance(attribute, ContinuousAttribute):
                try:
                    value1 = float(self.tableWidgetAA.item(i, 0).text())
                    print(f"P: value1: {value1}")
                    value2 = float(self.tableWidgetAA.item(i, 1).text())
                    if (float(attribute.value1) <= value1) and (float(attribute.value2) >= value2):
                        continue
                    else:
                        QMessageBox.warning(self, 'Warning', 'Some parametres are not within the range set out in the attribute.')
                        return
                except (ValueError, AttributeError):
                    QMessageBox.warning(self, 'Warning', 'Complete all values correctly.')
                    return

        for i,attribute in enumerate(self.attCD):
            if isinstance(attribute, ContinuousAttribute):
                value1 = self.tableWidgetAA.item(i, 0).text()
                value2 = self.tableWidgetAA.item(i, 1).text()
                element = ContinuousAttribute(value1=value1,value2=value2)
            elif isinstance(attribute, DiscreteAttribute):
                attNames = self.attCD[i]
                attNames = attNames.attributenames
                combo_box = self.tableWidgetAA.cellWidget(i,0)
                selected = combo_box.currentText()
                element = DiscreteAttribute(attributenames=attNames)
                element.selected = selected

            self.alternativeList.append(element)
        altName = self.textAlternativeName.toPlainText()
        altDesc = self.textAlternativeDescription.toPlainText()
        if altName and altDesc: 
            alternative = Alternative(name=altName,desc=altDesc,attr=self.alternativeList)
            alternatives.append(alternative)
            self.vAltCon = VentanaAltCon()
            self.vAltCon.show()
            self.close()
            

        else:
            QMessageBox.warning(self, 'Warning', 'The Alternative Name and Alternative Description field cannot be empty. It cannot be added.')
    
        

    def closeW(self):
        self.vAltCon = VentanaAltCon()
        self.vAltCon.show()
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
        # self.textUnits.textChanged.connect(self.update_label)
        # self.textMinRange.textChanged.connect(self.update_label)
        # self.textMaxRange.textChanged.connect(self.update_label)
        self.textName.textChanged.connect(self.update_label)
        self.buttonEnter.clicked.connect(self.create_table)
        self.textDescription.textChanged.connect(self.update_label)
        self.buttonApply.setEnabled(True)
        # self.buttonOk.clicked.connect(lambda: self.ok_button_clicked(self.sender()))
        self.spinBoxDiscrete.valueChanged.connect(lambda: self.onValueChanged)

        self.radioBCont.toggled.connect(self.disable_discrete)
        self.radioBDisc.toggled.connect(self.disable_continuous)

        # Hide or show Save and Cancel Buttons
        self.tabWidgetNI.currentChanged.connect(self.update_buttons)


            
        # self.textDescription.textChanged.connect(self.onTextChanged)
        # self.textLabel.textChanged.connect(self.onTextChanged)

        # self.textDescCont.textChanged.connect(self.onTextChanged)
        # self.textUnitsCont.textChanged.connect(self.onTextChanged)
        # self.textMinRangeCont.textChanged.connect(self.onTextChanged)
        # self.textMaxRangeCont.textChanged.connect(self.onTextChanged)
        # self.textDescDisc.textChanged.connect(self.onTextChanged)
        # self.textName.textChanged.connect(self.onTextChanged)


    


    def update_buttons(self, index):
        # Comprobamos qué pestaña está activa y mostramos/ocultamos los botones
        current_tab_name = self.tabWidgetNI.tabText(index)
        if current_tab_name == 'Leaf Information':
            self.buttonApply.show()
            self.buttonCancel.show()
        elif current_tab_name == 'Leaf Attribute':
            self.buttonApply.show()
            self.buttonCancel.show()
        elif current_tab_name == 'Viewing Component Utilities':
            self.buttonApply.hide()
            self.buttonCancel.hide()
        elif current_tab_name == 'Viewing Alternative Consequences':
            self.buttonApply.hide()
            self.buttonCancel.hide()
        elif current_tab_name == 'Subjective Scale':
            self.buttonApply.hide()
            self.buttonCancel.hide()
        elif current_tab_name == 'Quantifying Preferences':
            self.buttonApply.hide()
            self.buttonCancel.hide()
        else: # current_tab_name == 'Weight Stability Interval':
            self.buttonApply.hide()
            self.buttonCancel.hide()

    def update_label(self):
        self.buttonApply.setEnabled(False)
        self.textLabel.toPlainText()
        # self.parent().labels[identifier_labels-1].setText(text)

    def create_table(self):
        # Get number of rows
        self.buttonApply.setEnabled(True)
        reply = QMessageBox.warning(self.parent(),f'Modify Discrete Attribute', f'Are you sure you want to modify the options?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            num_rows = self.spinBoxDiscrete.value()
            # Create table with number of rows and two columns
            widthTable = self.tableDiscrete.width()
            self.tableDiscrete.setRowCount(num_rows)
            self.tableDiscrete.setColumnCount(1)
            self.tableDiscrete.setColumnWidth(0, widthTable)
            self.tableDiscrete.setHorizontalHeaderLabels(['Attributes'])
            
            # self.tableDiscrete.setColumnWidth(1, self.tableDiscrete.columnWidth(1) // 16)

            # Adding elements to the table
            for i in range(num_rows):
                # Add text in the first column
                item = QTableWidgetItem(f"Attribute {i+1}")
                self.tableDiscrete.setItem(i, 0, item)

                # Add option in second column
                # radio_button = QRadioButton()
                # radio_button.setObjectName(str(i))
                # self.tableDiscrete.setCellWidget(i, 1, radio_button)
                # self.tableDiscrete.cellWidget(i, 1).setStyleSheet('margin-left: 10px;') 

            
            # Select default option in the first row
            # first_radio_button = self.tableDiscrete.cellWidget(0, 1)
            # first_radio_button.setChecked(True)

        else: 
            pass

    def disable_discrete(self, state):
        # self.continu
        if state:
            self.textDescDisc.setEnabled(False)
            self.spinBoxDiscrete.setEnabled(False)
            self.buttonEnter.setEnabled(False)
            self.tableDiscrete.setEnabled(False)
        else:
            self.textDescDisc.setEnabled(True)
            self.spinBoxDiscrete.setEnabled(True)
            self.buttonEnter.setEnabled(True)
            self.tableDiscrete.setEnabled(True)

    def disable_continuous(self, state):
        if state:
            self.textDescCont.setEnabled(False)
            self.textUnitsCont.setEnabled(False)
            self.textMinRangeCont.setEnabled(False)
            self.textMaxRangeCont.setEnabled(False)
        else:
            self.textDescCont.setEnabled(True)
            self.textUnitsCont.setEnabled(True)
            self.textMinRangeCont.setEnabled(True)
            self.textMaxRangeCont.setEnabled(True)

    def onValueChanged(self):
        # Verificar si el valor del QSpinBox es mayor que cero
        if self.spinspinBoxDiscretebox.value() > 0:
            # Habilitar el QPushButton
            self.buttonEnter.setEnabled(True)
        else:
            # Deshabilitar el QPushButton
            self.buttonEnter.setEnabled(False)
            
    
    # def onTextChanged(self):
    #     self.buttonApply.setEnabled(True)
    #     self.textDescription.setPlainText(self.textDescription.toPlainText())
    #     self.textLabel.setPlainText(self.textLabel.toPlainText())

    #     self.textDescCont.setPlainText(self.textDescCont.toPlainText())
    #     self.textUnitsCont.setPlainText(self.textUnitsCont.toPlainText())
    #     self.textMinRangeCont.setPlainText(self.textMinRangeCont.toPlainText())
    #     self.textMaxRangeCont.setPlainText(self.textMaxRangeCont.toPlainText())
    #     self.textDescDisc.setPlainText(self.textDescDisc.toPlainText())
    #     self.textName.setPlainText(self.textName.toPlainText())
    


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
        
        # tipe of the node

        self.nodeDescription = ""
        
        # tipe of the unit

        self.unitType = ""
        self.unitDescription = ""
        self.unitName = ""
        self.minRange = 0
        self.maxRange = 1
        # self.optionDiscrete = "" 
        self.optionsList = []


        # connections between labels
        # self.connections = []


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
            self.connections.append(label)

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
        
        number_connection = len(parent.parent.labels[0].connections)
        numColumn = 0

        if number_connection == 0:
            numColumn = 0
        elif number_connection == 1:
            numColumn = 15
        elif number_connection == 2:
            numColumn = 30
        elif number_connection == 3:
            numColumn = 45
        elif number_connection == 4:
            numColumn = 60
        elif number_connection == 5:
            numColumn = 75
        elif number_connection == 6:
            numColumn = 90
        elif number_connection == 7:
            numColumn = 105


        labelLE = LabelNode(identifier= identifier_labels,text="Label"+str(identifier_labels),label_name= "Label"+str(identifier_labels),
                            posArray=len(parent.parent.labels),cRow=numColumn,cColumn=2)
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
        
        parent.parent.layout.addWidget(labelLE,numColumn,2)
        currentColumn += 1
        Branch+=1
        sonsPO = parent.parent.labels[0]
        print(f"P: Tipo de Objeto: {sonsPO}")
        sonsPO.add_connection(labelLE)
        
        print(f"P: Numero de conexiones padre: {number_connection}")


        print("P: Number of Labels: "+str(len(parent.parent.labels)))
        labelLE.double_clicked.connect(parent.parent.open_NodeInfo)

        central_pos = math.floor(currentRow/2)
        parent.parent.layout.addWidget(parent.parent.labels[0], central_pos-1, 0)
        parent.parent.layout.update()
        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)


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

        rowS = labelAnc.cRow + posA

        print(f"P: rowS: {rowS}")
        labelLE = LabelNode(identifier= identifier_labels,text="Label"+str(identifier_labels),label_name= "Label"+str(identifier_labels),
                            posArray=len(parent.parent.labels),cRow=rowS,cColumn=labelAnc.cColumn+2)
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
        
        widget = parent.parent.layout.itemAtPosition(labelLE.cRow,labelLE.cColumn)
        if widget is None:
            parent.parent.layout.addWidget(labelLE,labelLE.cRow,labelLE.cColumn)
        else:
            labelLE.cRow +=1
            parent.parent.layout.addWidget(labelLE,labelLE.cRow,labelLE.cColumn)
            
        # prueba para ver si está ocupada una posición del layout

        # widget = parent.parent.layout.itemAtPosition(labelLE.cRow,labelLE.cColumn)
        # if widget is None:
        #     print("La posición de labelLE está vacía")
        # else:
        #     print("La posición labelLE está ocupada")

        currentColumn+=1
        
        
        labelAnc.add_connection(labelLE)
        labelAnc = parent.parent.labels[self.posArray]
        print("P: Number of Labels: "+str(len(parent.parent.labels)))
        labelLE.double_clicked.connect(parent.parent.open_NodeInfo)
        print(f"Número de hijos del nodo anterior: {len(labelAnc.connections)}")
        
        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)
        # central_pos = math.floor(Branch/2)
        # parent.parent.layout.addWidget(parent.parent.labels[0], central_pos-1, 0)
        # parent.parent.layout.update()
        # print(f"{parent.parent.labels}")

    # def count_items_above(self, row, col):
    #         parent = self.parent()
    #         count = 0
    #         while row > 0:
    #             row -= 1
    #             item = parent.parent.layout.itemAtPosition(row, col)
    #             if item is not None:
    #                 count += 1
    #             else:
    #                 break
    #         return count


    # returns the final Nodes attributes

    def getFinalAttributes(self, finalNodes):
        global attributes
        parent = self.parent()
        attributes = []
        for node in finalNodes:
            if not node.connections:
                attributes.append(node)


    def create_lines_layout(self):
        parent = self.parent()
        label_item_connections = 0

        for line in parent.parent.lineB:
            try:
                line.deleteLater()
                parent.parent.lineB.pop(line)
            except:
                pass

        for line in parent.parent.lines:
            try:
                line.deleteLater()
                parent.parent.lines.pop(line)

            except:
                pass
            # parent.parent.layout.removeWidget(line)
        if not parent.parent.labels:
            return

        labelPO = parent.parent.labels[0]
        if labelPO is not None and labelPO.connections:
            connection_listPO = labelPO.connections
            for k in range(len(connection_listPO)):
                if k == 0:
                    line = DLineFrameB()
                    parent.parent.layout.addWidget(line, 0, 1, 3, 1)
                    line.lower()
                    parent.parent.lineB.append(line)

                else: 
                    numero = k * 15
                    connection = connection_listPO[k]
                    line = DLineFrame(dRow=labelPO.cRow,dColumn=connection.cColumn-1,dNum=numero-1)
                    line.dRow = labelPO.cRow
                    line.dColumn = connection.cColumn-1
                    line.dNum = numero-1
                    parent.parent.layout.addWidget(line,line.dRow,line.dColumn,line.dNum,2)
                    line.lower()
                    parent.parent.lines.append(line)

            

        for i in range(1,len(parent.parent.labels)):
            label = parent.parent.labels[i]

            # label_item = parent.parent.layout.itemAtPosition(label.cRow-1,label.cColumn).widget()
            # label_item_connections = len(label_item.connections)
            
            if label.connections:
                for j in range(len(label.connections)):
                    numero = label.cRow
                    resultado = numero % 15
                    for i in range(15, 151, 15):
                        if numero >= i:
                            resultado = numero % i
                    for i in range(resultado):
                        label_item = parent.parent.layout.itemAtPosition(label.cRow-i,label.cColumn)
                        
                        if hasattr(label_item,'connections'):
                            label_item = label_item.widget()
                            label_item_connections = len(label_item.connections)
                        else:
                            return

                    numero = label_item_connections 
                    connection_list = label.connections
                    connection = connection_list[j]
                    if label.cRow == connection.cRow:
                        line = HLineFrame()
                        parent.parent.layout.addWidget(line,label.cRow,connection.cColumn-1,1,2)
                    else:
                        line = DLineFrame(dRow=label.cRow,dColumn=connection.cColumn-1,dNum=numero+j+1)
                        parent.parent.layout.addWidget(line,label.cRow,connection.cColumn-1,numero+j+1,2)
                    line.lower()
                    parent.parent.lines.append(line)

        parent.parent.layout.update()

        


    def deleteLabelPO(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        
        parent = self.parent()
        self.create_lines_layout()
        
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
            self.create_lines_layout()

        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)

    # recursive method for subtracting -15 from each row in each label 


    def update_cRow(self,label):
        parent = self.parent()
        self.create_lines_layout()
        for conn in label.connections:
            print("P: Cuántas veces accede a la función recursiva -------")
            conn.cRow -= 15
            parent.parent.layout.addWidget(conn, conn.cRow,conn.cColumn)
            parent.parent.layout.update()
            self.update_cRow(conn)
        self.getFinalAttributes(parent.parent.labels)


    # def update_cRow(self,label):
    #     stack = [label]
    #     while stack:
    #         node = stack.pop()
    #         for conn in node.connections:
    #             conn.cRow -= 15
    #             stack.append(conn)


    def deleteLabelSon(self):
        global PrimaryObjective
        global currentColumn
        global currentRow
        global Branch
        global identifier_labels
        global Leaf
        
        parent = self.parent()

        label_remove = parent.findChildren(QLabel,self.objectName())[self.posArray]

        self.create_lines_layout()
 

        if not label_remove.connections:
            reply = QMessageBox.warning(self.parent(),f'Delete Leaf {label_remove.label_name}', f'Are you sure you want to delete {label_remove.label_name}?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        else:
            reply = QMessageBox.warning(self.parent(),f'Delete Intermediate Node {label_remove.label_name}', f'Are you sure you want to delete {label_remove.label_name}? If you delete it, all the connected elements to {label_remove.label_name} will be deleted.',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.No:
            pass
        else:

            # with these loops I want to subtract -15 from all subsequent rows

            found_index = None
            for i, label in enumerate(parent.parent.labels[0].connections):
                if label.text() == label_remove.text():
                    found_index = i
                    break

            if found_index is not None:
                for label in parent.parent.labels[0].connections[found_index+1:]:
                    if label.connections:
                        label.cRow -= 15
                        self.update_cRow(label)
                    else: 
                        label.cRow-= 15

            for label in parent.parent.labels:            
                parent.parent.layout.addWidget(label, label.cRow, label.cColumn)
                parent.parent.layout.update()

            self.create_lines_layout()

            print(f"P: {parent.parent.labels}")
            print(f"P: Label: {label_remove}")

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
                    # print(parent.parent.labels)
                    
            else:
                label_remove.remove_label(label_remove)


        print(f"P: {parent.parent.labels}")

        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)
        
        
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

        self.create_lines_layout()
        self.getFinalAttributes(parent.parent.labels)


    # for every new node that is created dynamically

    def changeStyleSheet(self):
        if self.finalNode:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #7CEE69;")
        else:
            self.setStyleSheet(
                "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;")
            
            
    # when we import a new project so that every final node is marked
    
    
   
    def __repr__(self):
        return f"LabelNode({self.text()})"


# class InitialOptionLabels(QPushButton):
#     def __init__(self,text):
#         super().__init__(text)
#         self.setGeometry(130, 210, 101, 21)
#         self.setMinimumSize(131,21)
#         self.setMaximumSize(131,21)
#         self.setText(text)
#         self.setStyleSheet(
#             "background-color: #AAA8A8; border-radius: 6px; border: 1px solid #1F1F1F;")
#         self.show()

# horizontal line

class HLineFrame(QFrame):
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 0.79, Qt.PenStyle.SolidLine))
        y = self.height() // 2
        painter.drawLine(0, y, self.width(), y)


# down diagonal line

class DLineFrame(QFrame):
    def __init__(self, dRow=0, dColumn=0, dNum=0):
        super().__init__()
        self.dRow = dRow
        self.dColumn = dColumn
        self.dNum = dNum
        self.dDist = 2
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 1.2, Qt.PenStyle.SolidLine))
        painter.drawLine(-10, 18, self.width()-100, self.height()-10)

    def __repr__(self):
        return f"DLineFrame({self.dRow},{self.dColumn},{self.dNum},{self.dDist})"
 
# upper diagonal line

class DLineFrameB(QFrame):
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QBrush(QColor("black")), 1.2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.drawLine(-100, self.height(), self.width(), 20)
        
        self.dbRow = 0
        self.dbColumn = 1
        self.dbNum = 3
        self.dbDist = 1 
    
    def __repr__(self):
        return "DLineFrameB()"

# we create two classes: one for discrete and another for continuous

class ContinuousAttribute:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2

    
    def __repr__(self):
        return f"ContinuousAttribute: {self.value1}, {self.value2};"



class DiscreteAttribute:
    def __init__(self, attributenames):
        self.attributenames = attributenames
        self.selected = ""

    def __repr__(self):
        return f"DiscreteAttribute: Nº Options{len(self.attributenames)}, {self.selected}"


class Alternative:
    def __init__(self, name, desc, attr):
        self.name = name
        self.desc = desc
        self.attr = attr


    def __repr__(self):
        return f"Alternative: {self.name}"



if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaLogIn()
    GUI.show()
    sys.exit(app.exec())
