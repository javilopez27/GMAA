import sys
from PyQt6.QtWidgets import QApplication,QInputDialog, QGraphicsView, QGraphicsView, QFrame, QWidget,QToolBar, QMainWindow, QFileDialog, QLabel, QMenu, QPushButton, QVBoxLayout, QStatusBar, QHBoxLayout, QLineEdit, QMessageBox
from PyQt6.QtGui import QIcon, QFont, QCursor, QAction, QShortcut, QKeySequence, QColor, QPalette, QPainter, QMouseEvent
from PyQt6.QtCore import QTimer, Qt, QPoint, QUrl, QSize, QPoint, pyqtSignal, pyqtSlot
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6 import uic
from ui_aboutGMAA import Ui_AboutGMAA
from ui_guiGMAA import Ui_MainWindow
from ui_LogIn import Ui_LogIn
from ui_nodeInformation import Ui_MainWindow
import networkx as nx # With this library we can save and import any proyect thanks to XML
import xml.etree.ElementTree as ET # With this library we can import the proyect 
import os 

PrimaryObjective = False
Branch = 0
Leaves = 0
identifier_labels = 0

root = ET.Element("QLabels")

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

        #

        # self.botonDesactivar = self.findChild(QPushButton, "botonDesactivar")

        # we found all the new labels created
        self.labels = []

        # Saves the previous value in the Save QInputDialog 
        self.previous_value = None

        # Context Menu Creation
        self.context_menuPO = QMenu(self)

        # Habilitar menú contextual en el widget principal
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menuPO)

        # Action to create the PrimaryObjective Label
        self.actionCPO = QAction("Create a Primary Objective", self)
        # create_PO function to create the PO first Label
        self.actionCPO.triggered.connect(self.create_PO)

        # Action to create the Brach/Leaves Labels
        self.actionCBL = QAction("Create Branches/Leaves", self)
        self.actionCBL.triggered.connect(self.create_BL)

        # Action to delete the Primary Objective Label
        self.actionDPO = QAction("Delete Primary Objective", self)
        self.actionDPO.triggered.connect(self.delete_PO)

        # Adding actions to de the Context Menu Created
        self.context_menuPO.addAction(self.actionCPO)

        # connect Menu signals
        self.actionCredits.triggered.connect(self.fn_help)
        self.actionLogIn.triggered.connect(self.fn_login)
        self.actionSave_WorkSpace.triggered.connect(self.save_proInput)
        self.actionSave_WorkSpace_As.triggered.connect(self.save_proInput)
        self.actionClose_WorkSpace.triggered.connect(self.close_workspace)


        # connect Toolbar signals
        # self.actionNew_Workspace.triggered.connect(self.new_workspace)
        self.actionOpen_Workspace.triggered.connect(lambda: self.open_workspace)
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

    def open_workspace(self):
        # options = QFileDialog.options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo XML", "", "Archivos XML (*.xml)")
        if file_name:
            # Procesar el archivo XML aquí
            print("Archivo seleccionado:", file_name)



    # def is_save(self):
    #     if not self.textEdit.document().isModified():
    #         return True

    #     ret = QMessageBox.warning(self, "GMAA WorkSpace", "The WorkSpace Document has been modified. \n Do you want to save changes?",QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |QMessageBox.StandardButton.Cancel)

    #     if ret == QMessageBox.StandardButton.Save:
    #         return self.save_workspace()

    #     if ret == QMessageBox.StandardButton.Cancel:
    #         return False

    #     return True
    

    def save_proInput(self): 
        
        default_value = self.previous_value if self.previous_value is not None else ''
        file_name, ok = QInputDialog.getText(self, "Save Project", "Insert name's project:",text=default_value)
        valueF = file_name
        file_name = file_name + ".xml"   # We add the XML extension
        if ok:
            self.previous_value = valueF
            self.save_project(file_name)


    def save_project(self, file_path):
        root = ET.Element("Project GMAA")
        for label in self.labels:
            print("P: Label_name "+str(label.label_name))
            root.append(label.to_xml())

        tree = ET.ElementTree(root)
        tree.write(file_path)


    # What this function does is to ask you what you want to do when you save your workspace 

    def close_workspace(self,event):
        global PrimaryObjective
        global identifier_labels

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
        if PrimaryObjective == True:
            self.context_menuPO.removeAction(self.actionCPO)
            # Adding the Action of creating branches and leaves
            self.context_menuPO.addAction(self.actionCBL)
            # Adding the Action of creating branches and leaves
            self.context_menuPO.addAction(self.actionDPO)
        elif PrimaryObjective == False:
            self.context_menuPO.addAction(self.actionCPO)
        self.context_menuPO.exec(self.mapToGlobal(point))

    def create_PO(self):

        global Leaves
        global identifier_labels
        global PrimaryObjective
        PrimaryObjective = True

        
        labelPO = LabelNode(identifier = identifier_labels, text="PO Label",label_name= "PO Label"+str(identifier_labels))
        identifier_labels += 1
        self.labels.append(labelPO) # adds PO Label to the list of mainwindow labels
        print("P: Number of Labels: "+str(len(self.labels)))
        self.actionSaveWorkspace.setEnabled(True)
        self.actionSave_WorkSpace.setEnabled(True)
        self.actionSave_WorkSpace_As.setEnabled(True)
        print("P: Nodes Identifier is "+str(labelPO.identifier))
        # print("P: "+str(self.labels[identifier_labels-1].label_name))
        Leaves = Leaves + 1
        labelPO.setVisible(True)
        labelPO.setFixedSize(120, 40)
        # self.setCentralWidget(labelPO)
        self.labels[identifier_labels-1].move(200, 100)
        # labelPO.double_clicked.connect(lambda: self.open_NodeInfo(labelPO.identifier))
        labelPO.double_clicked.connect(self.open_NodeInfo)
        
        # XML with ElementTree so that we can save it

    
    def open_NodeInfo(self):
        vNodeInfo = VentanaNodeInfo(self)
        # labelPO = self.labels[identifier]
        # identifier_label = labelPO.identifier
        # vNodeInfo.update_label(identifier_label)
        # vNodeInfo
        vNodeInfo.show()

    # Functions to implement

    def create_BL(self):
        global Leaves
        global identifier_labels
        global PrimaryObjective
        PrimaryObjective = True

        labelLE = LabelNode(identifier= identifier_labels,text="Label",label_name= "Label"+str(identifier_labels))
        identifier_labels+=1
        self.labels.append(labelLE)
        print("P: Number of Labels: "+str(len(self.labels)))
        print("P: Nodes Identifier is "+str(labelLE.identifier))
        Leaves = Leaves + 1
        labelLE.setVisible(True)
        labelLE.setFixedSize(120, 40)
        self.setCentralWidget(labelLE)
        print("P: Number of Labels: "+str(len(self.labels)))
        labelLE.double_clicked.connect(self.open_NodeInfo)
        
    def delete_PO(self):
        pass

    # def closeEvent(self,event):
    #     if self.textEdit.toPlainText():
    #         reply = QMessageBox.warning(self, "GMAA WorkSpace", "The WorkSpace Document has been modified. \n Do you want to save changes?", QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Save)

    #         if reply == QMessageBox.StandardButton.Discard:
    #             event.accept()

    #         if reply == QMessageBox.StandardButton.Save:
    #             event.ignore()
    #             self.save_workspace()
    #             self.close_window()

    #         if reply == QMessageBox.StandardButton.Cancel:
    #             event.ignore()

    #     else:
    #         event.accept()

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
        palette = QPalette()
        color = QColor(255, 255, 255)  # Color Blanco
        palette.setColor(QPalette.ColorRole.Text, color)
        self.lineUser.setPalette(palette)
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
        if self.lineUser.text() == 'javier' and self.linePw.text() == 'lopez':
            self.close()


class VentanaNodeInfo(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaNodeInfo, self).__init__(parent)
        uic.loadUi("nodeInformation.ui", self)
        icono = QIcon("iconoUPM.ico")
        super(VentanaNodeInfo, self).setWindowIcon(icono)
        super(VentanaNodeInfo, self).setWindowTitle("Node Information")
        self.VentanaPrincipalGMAA = parent
        
        self.buttonCancel.clicked.connect(self.close_windowNI)
        self.textLabel.textChanged.connect(self.update_label)

    def update_label(self):
        text = self.textLabel.toPlainText()
        self.parent().labels[identifier_labels-1].setText(text)

    # def update_textLabel_text(self):
    #     self.text = self.textLabel.toPlainText()
    #     self.textLabel.setText(self.text)

    def close_windowNI(self):
        self.close()



class LabelNode(QLabel):
    # connect signals
    double_clicked = pyqtSignal()

    def __init__(self, identifier, text, label_name, parent=None):
        super().__init__(text, parent)
        global PrimaryObjective
        PrimaryObjective = True
        self.VentanaPrincipalGMAA = parent
        # Mouse Tracking
        self.setMouseTracking(True)
        self.setObjectName("MyLabel")
        self.clicked = False
        self.identifier = identifier
        self.label_name = label_name
        self.connections = []  # this are connections between nodes to know which ones are related
        self.setGeometry(130, 210, 131, 41)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFrameShape(QLabel.Shape.Box)
        self.setFrameShadow(QLabel.Shadow.Sunken)
        if PrimaryObjective == True:
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
    
    def showContextMenu(self, pos):
        global Leaves
        global identifier_labels

        menu = QMenu()
        action_name = QAction("Name: "+str(self.text()), self)
        action_label = QAction("Label: "+str(self.label_name), self)
        print("P: Number of Leaves now: "+str(Leaves))
        action_createSon = QAction("Create a son", self)

        action_createSon.triggered.connect(self.create_BL)
        # delete_action.triggered.connect(self.parent().)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.deleteLabel) 
        menu.addAction(action_name)
        menu.addAction(action_label)
        menu.addSeparator()
        menu.addAction(action_createSon)
        menu.addAction(delete_action)
        menu.exec(self.mapToGlobal(pos))

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

    def to_xml(self):
        element = ET.Element("MyLabel")
        element.set("text", self.text())
        element.set("x", str(self.pos().x()))
        element.set("y", str(self.pos().y()))
        element.set("width", str(self.size().width()))
        element.set("height", str(self.size().height()))
        element.set("id",str(self.identifier))
        element.set("label_name",self.label_name)
        return element
    
    def create_BL(self):
        # print("P: Entra en la función de create_BL")
        # global Leaves
        # global identifier_labels
        # global PrimaryObjective
        # PrimaryObjective = True 

        # labelLE = LabelNode(identifier= identifier_labels,text="Label",label_name= "Label"+str(identifier_labels))
        # identifier_labels+=1
        # self.parent().labels.append(labelLE)
        # print("P: Number of Labels: "+str(len(self.labels)))
        # print("P: Nodes Identifier is "+str(labelLE.identifier))
        # Leaves = Leaves + 1
        # labelLE.setVisible(True)
        # labelLE.setFixedSize(120, 40)
        # self.setCentralWidget(labelLE)
        # labelLE.double_clicked.connect(self.open_NodeInfo)
        pass

    def deleteLabel(self):
        global PrimaryObjective
        PrimaryObjective = False
        Leaves = 0  # if the delete button of the PO Label is triggered the num of Leaves is 0
        identifier_labels = 0
        self.parent().labels.clear()
        print("P: Number of active Labels: "+str(len(self.parent().labels)))
        self.parent().actionSaveWorkspace.setEnabled(False)
        self.parent().actionSave_WorkSpace.setEnabled(False)
        self.parent().actionSave_WorkSpace_As.setEnabled(False)
        self.deleteLater()


    # def deleteLabelPO(self):
    #     self.deleteLater
    #     global PrimaryObjective
    #     PrimaryObjective = False



if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaPrincipalGMAA()
    GUI.show()
    sys.exit(app.exec())
