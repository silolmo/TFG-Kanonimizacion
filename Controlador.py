import subprocess, csv, itertools
import TableModel

from Vistas.TableWindow import * 
from Vistas.ImportDialog import *
from Vistas.HierarchyDialog import *
from Vistas.ResultsWindow import *
from Vistas.InicioWindow import *
from BD import *
from ModelNode import Node

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QLabel,
    QDialog,
    QMainWindow,
    QSpinBox,
    QMessageBox,
    QComboBox,
    QTableWidgetItem, 
    QGridLayout,
    QButtonGroup,
    QRadioButton,
    QFileDialog
)
class Inicio(QMainWindow, Ui_InicioWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self) 
        self.resize(width,height)
        self.label_3.setMaximumWidth(width-(self.label.width()+self.label_2.width()))
        self.pushButton.clicked.connect(self.openApp)   

    def openApp(self):
        window.show() 
        self.close()  

class Table(QMainWindow, Ui_TableWindow): 
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self) 
        self.resize(width,height)
        self.label_sensitive.setHidden(True)
        self.label_identificator.setHidden(True)
        self.dialogImport = Import(self)
        self.dialogHierarchy = Hierarchy(self)
        self.windowResults = Results()
        self.setNonSensibles()
        self.setData()
        self.button_saveAttributes.clicked.connect(self.saveAttributesTypes)
        self.button_data.clicked.connect(self.showDialogImport)
        self.button_hierarchy.clicked.connect(self.showDialogHierarchy)
        self.button_anonymize.clicked.connect(self.anonymity)
        self.button_propuestaCuasi.clicked.connect(self.propuestaCuasi)
        self.attributes_anonimation = []
        self.inicio = Inicio()
        self.inicio.show()
  
    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                 'Cerrar',
                                 "Si cierra la aplicación todos los datos cargados se borrarán, ¿realmente desea cerrar la aplicacion?",
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            bd.drop_tables()
        else:
            event.ignore()

    def setData(self):
        self.headers = []
        if bd_data.exist():
            cur = bd_data.getData()
            self.data = cur.fetchall()

            cur = bd_data.getColumnsNames()
            for table in cur.fetchall():
                self.headers.append(str(table[0]))
            model = TableModel.TableModel(self.data, self.headers)
            self.tableView.setModel(model)
            self.dialogHierarchy.setData(self.data)
        else:
            #Clear
            self.tableView.setModel(TableModel.TableModel([''],['']))

        while self.gridLayout_sensitives.count()>4:
            self.gridLayout_sensitives.itemAt(4).widget().setParent(None)
        if(self.headers):
            self.label_sensitive.setHidden(False)
            self.label_identificator.setHidden(False)
            for header in self.headers:
                label = QtWidgets.QLabel(f'{header}')
                label.setObjectName(f'label_{header}')
                checkbox_sensitive = QtWidgets.QCheckBox()
                checkbox_identificator = QtWidgets.QCheckBox()
                self.gridLayout_sensitives.addWidget(label)
                self.gridLayout_sensitives.addWidget(checkbox_sensitive)
                self.gridLayout_sensitives.addWidget(checkbox_identificator)
                
                if(bd_attributes.exist()):
                    if(bd_attributes.getTipo(header)== 'Sensible'):
                        checkbox_sensitive.setChecked(True)
                    elif(bd_attributes.getTipo(header)== 'Identificador'):
                        checkbox_identificator.setChecked(True) 
        self.setNonSensibles()

    def showDialogImport(self):
        self.dialogImport.show()
        
    def showDialogHierarchy(self):
        if(bd_attributes.exist() and len(bd_attributes.getNonSensible())>0):
            self.dialogHierarchy.addContent()
            self.dialogHierarchy.show()
        else:
            QMessageBox.about(self, "Añade atributos cuasi-identificadores", "Solo se puede agregar jerarquía de generalización a los atributos cuasi-identificadores")
    
    def refresh(self):
        self.setData()
    
    def anonymity(self):
        #Inicializo los datos
        Q = [] #Cuasiidentiicadores
        for i in range(self.formLayout_cuasi.rowCount()+1):
            if(i>1):
                checkbox = self.formLayout_cuasi.itemAt(i)
                if(checkbox.widget().isChecked()):
                    Q.append(checkbox.widget().text())
        k = self.spinBox.value() # Valor de k para la k-anonimización
        numQ = len(Q) # número de cuasiidentificadores
        S = [Node([])] # Lista de nodos candidatos
        queue = [] # Cola de nodos a comprobar
        
        # Compruebo si tengo todos los datos necesarios para realizar el algoritmo
        allData = True
        if(numQ==0):
            allData = False
        for attribute in Q:
            if(bd_hierarchy.exist(attribute)==False):
                allData = False
        
        # Si tengo todos los datos comienzo
        if(allData):            
            if(Q != self.attributes_anonimation):
                bd.dropAlgorithmData()
    
            for i in range(1, numQ+1): # Se repite tantas veces como cuasiidentificadores tengo
                aux = S.copy()
                S.clear()
                for a in aux: # Recorro todos los nodos candidatos de nivel i-1 y los aumento el nivel
                    for j in range(bd_hierarchy.levels(Q[i-1])+1):  # A un nodo [0,2] -> [0,2,0], [0,2,1], [0,2,2]
                        b = a.getValue().copy()
                        b.append(j)
                        S.append(b) 
                        
                if(bd_nodes.exist(i)==False):
                    bd_nodes.create(i, S, Q)
                if(bd_edges.exist(i)==False):
                    bd_edges.create(i)
                C = bd_nodes.getData(i)
                E = bd_edges.getData(i)

                S = C.copy()

                for node in S:
                    if node.getRoot():
                        queue.insert(0, node)
                
                while(len(queue)!=0):
                    node = queue.pop()
                    if(node.getMark()==False):
                        if(node.getRoot()==True):
                            frequencySet = Node.getFrequencySetByDimension(Q,i)
                            frequencySet = Node.getFrequencySetByFather(Q, frequencySet, node)
                            node.setFrequencySet(frequencySet)
                        else:
                            fathers = node.getFathers()
                            frequencyFather = fathers[0].getFrequencySet()
                            while (frequencyFather==None):
                                while len(fathers)!=0:
                                    father = fathers.pop()
                                    frequencyFather = father.getFrequencySet()
                                    if(frequencyFather!=None):
                                        break
                                fathers = father.getFathers()

                            frequencySet = Node.getFrequencySetByFather(Q, frequencyFather, node)
                            node.setFrequencySet(frequencySet)

                        # Comprobar k-anonimato del nodo
                        if(node.getValue()==[2,1,0]):
                            print(frequencySet)
                        values = frequencySet.values()
                        anonymity = (k <= min(values))
                        if(anonymity):
                            # Marcar generalizaciones directas del nodo
                            node_end = bd_nodes.getNodeFin(i)
                            nodes_consecutivos = bd_nodes.getNodesConsecutivos(node.getValue(), node_end)
                            for n in nodes_consecutivos:
                                for item in S:
                                    if(item.getValue()==n):
                                        item.setMark(True)
                                        item.setFather(node)
                                        break
                        else:
                            S.remove(node)
                            node_end = bd_nodes.getNodeFin(i)
                            nodes_consecutivos = bd_nodes.getNodesConsecutivos(node.getValue(),node_end)
                            for n in nodes_consecutivos:
                                exist = False
                                for item in queue:
                                    if(item.getValue()==n):
                                        exist = True
                                if(exist==False):
                                    for item in S:
                                        if(item.getValue()==n):
                                            item.setFather(node)
                                            queue.insert(0, item)
                                            break
                
                if(len(S)==0):
                    break
        
            if(S):
                self.windowResults.setGeneralizations(S)
                self.windowResults.setInitialData(self.headers, self.data, Q)
                self.windowResults.show()
            else:
                QMessageBox.about(self, "No hay generalizaciones candidatas", "No hay generalizaciones candidatas para los atributos y el valor de k indicado") 
        else:
            QMessageBox.about(self, "Faltan datos para la anonimización", "Introduce los atributos cuasi-identificadores y sus respetivas jerarquías para poder anonimizar los datos") 

    def setNonSensibles(self):
        while self.formLayout_cuasi.rowCount()>1:
            self.formLayout_cuasi.removeRow(1)

        if(bd_attributes.exist()):
            nonSensibles = bd_attributes.getNonSensible()
            for item in nonSensibles:
                checkbox = QtWidgets.QCheckBox(f'{item}')
                checkbox.setObjectName(f'checkbox_{item}')
                self.formLayout_cuasi.addRow(checkbox)

    def saveAttributesTypes(self):
        bd.dropAlgorithmData()

        if(bd_attributes.exist()):
            bd_attributes.clear()

        for i in range(4, self.gridLayout_sensitives.count(), 3):         
            label = self.gridLayout_sensitives.itemAt(i)
            checkbox_sensitive = self.gridLayout_sensitives.itemAt(i+1)
            checkbox_identificator = self.gridLayout_sensitives.itemAt(i+2)

            if(checkbox_sensitive.widget().isChecked()):
                bd_attributes.insert(label.widget().text(),'Sensible') 
            elif (checkbox_identificator.widget().isChecked()):
                bd_attributes.insert(label.widget().text(),'Identificador')
            else:
                bd_attributes.insert(label.widget().text(),'No sensible') #El atributo no es sensible/identificador
        self.setData()
        self.setNonSensibles()

        QMessageBox.about(self, "Actualización correcta", "Se han actualizado correctamente los tipos de los atributos") 

    def propuestaCuasi(self):
        percent = 0.05
        NonSensibles = bd_attributes.getNonSensible()        
        PS = []
        for i in range(1,len(NonSensibles)+1):
            for item in itertools.combinations(NonSensibles, i):
                PS.append(item)
        
        PS_value = {}
        for item in PS:
            PS_value[item] = len(Node.getFrequencySetByDimension(item, len(item)))

        maximum = max(PS_value.values())     
        maximum = maximum - (maximum*percent)
        quasiidentifiers = []
        for key, value in PS_value.items():
            if(value >= maximum):
                quasiidentifiers = key
                break

        messageBox = QMessageBox()
        messageBox.setWindowTitle('Propuesta de cuasi-identificadores')
        messageBox.setText (f'La propuesta de atributos cuasi-identificadores es: {quasiidentifiers}')
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText ('Aceptar')
        buttonN = messageBox.button(QMessageBox.No)
        buttonN.setText ('Cancelar')
        messageBox.exec_()
        if messageBox.clickedButton() == buttonY:
            for i in range(self.formLayout_cuasi.rowCount()+1):
                if(i>1):
                    checkbox = self.formLayout_cuasi.itemAt(i)
                    if(checkbox.widget().text() in quasiidentifiers):
                        checkbox.widget().setChecked(True)
                    else:
                        checkbox.widget().setChecked(False)

class Import(QDialog, Ui_ImportDialog):
    def __init__(self, *args, **kwargs):
        super(Import, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.saveAttributesTypes)
        self.button_openData.clicked.connect(self.openData)
        self.button_openAttributes.clicked.connect(self.openAttributes)
        self.button_addTypes.clicked.connect(self.addAttributesTypes)
        self.button_exportar.clicked.connect(self.exportAttributesTypes)
        self.label_2.setHidden(True)
        self.label_3.setHidden(True)
        self.label_4.setHidden(True)
        self.button_exportar.setHidden(True)

    def openData(self):
        archivo = QFileDialog.getOpenFileName(self, 'Abrir archivo', '~/Escritorio', "(*.csv *.txt)")
        if(len(archivo[0])>0):
            self.edit_data.setText(archivo[0])

    def openAttributes(self):
        archivo = QFileDialog.getOpenFileName(self, 'Abrir archivo', '~/Escritorio', "(*.csv *.txt)")
        if(len(archivo[0])>0):
            self.edit_attributes.setText(archivo[0])        

    def importData(self):
        bd.drop_tables()

        attributes = f''
        if (len(self.edit_attributes.text())==0):
            attributes = 'attributes.txt'
        else:
            attributes = self.edit_attributes.text()

        print(self.edit_data.text(), attributes, self.edit_separator.text())
        if(self.edit_data.text!=''):
            result = subprocess.run(['bash','import.sh', self.edit_data.text(), attributes, self.edit_separator.text()])
        if(result.returncode==0):
            QMessageBox.about(self, "Importación correcta", "Se han importado correctamente los datos del fichero"+self.edit_data.text())
            window.refresh()          
            bd_attributes.create()
        else:
            QMessageBox.about(self, "Importación incorrecta", "Ha habido un error al importar los datos del fichero"+self.edit_data.text())
            bd.drop_tables()

    def addAttributesTypes(self):
        if(self.edit_data.text()=='' or self.edit_separator.text()==""):
            QMessageBox.about(self, "Error" ,"Para añadir los tipos de los atributos primero tienes que indicar el archivo que contiene los datos y el separador")
        else:
            f = open(f"{self.edit_data.text()}", "r")
            line = f.readline()
            attributes = line.split(f'{self.edit_separator.text()}')
            attributes[len(attributes)-1] = attributes[len(attributes)-1].split('\n')[0]
            self.setData(attributes)
            f.close()
            self.edit_attributes.setText('')
        
    def setData(self, attributes):
        while self.gridLayout_types.count()>3: 
            self.gridLayout_types.itemAt(3).widget().setParent(None)

        self.label_2.setHidden(False)
        self.label_3.setHidden(False)
        self.label_4.setHidden(False)
        self.button_exportar.setHidden(False)
        for i in range(len(attributes)):
            label = QLabel()
            label.setText(f'{attributes[i]}')
            comboBox = QComboBox()
            comboBox.addItems(['varchar', 'char', 'int', 'double', 'boolean'])
            spinBox = QSpinBox()
            self.gridLayout_types.addWidget(label, i+1, 0)
            self.gridLayout_types.addWidget(comboBox, i+1, 1)
            self.gridLayout_types.addWidget(spinBox, i+1, 2)

    def saveAttributesTypes(self):
        if(self.gridLayout_types.rowCount()>1):
            f = open('attributes.txt', 'w')
            line = f''
            for i in range(1, self.gridLayout_types.rowCount()):
                type = self.gridLayout_types.itemAtPosition(i, 1).widget().currentText()
                lon = self.gridLayout_types.itemAtPosition(i, 2).widget().text()
                if(i==1):
                    line = line + f'{type}' + f'({lon})'
                else:
                    line = line + f', {type}' + f'({lon})'
            f.write(line)
            f.close()
        self.importData()

    def exportAttributesTypes(self):
        if(self.gridLayout_types.rowCount()>1):
            archivo = QFileDialog.getSaveFileName(self, 'Exportar tipos de atributos', '~/Escritorio', "(*.csv *.txt)")
            if('.' in archivo[0]):
                f = open(archivo[0], 'w')
            else:
                f = open(f'{archivo[0]}.txt', 'w')
            line = f''
            for i in range(1, self.gridLayout_types.rowCount()):
                type = self.gridLayout_types.itemAtPosition(i, 1).widget().currentText()
                lon = self.gridLayout_types.itemAtPosition(i, 2).widget().text()  
                if(i==1):
                    line = line + f'{type}' + f'({lon})'
                else:
                    line = line + f', {type}' + f'({lon})'
            f.write(line)
            f.close()

class Hierarchy(QDialog, Ui_HierarchyDialog):
    def __init__(self, *args, **kwargs):
        super(Hierarchy, self).__init__(*args, **kwargs)
        self.setupUi(self)        
        self.conjuntos = []
        self.button_guardar.clicked.connect(self.createHierarchies)
        self.button_add.clicked.connect(self.addLevel)
        self.button_delete.clicked.connect(self.deleteLevel)
        self.button_import.clicked.connect(self.importHierarchy)
        self.button_export.clicked.connect(self.exportHierarchy)
        self.button_suppression.clicked.connect(self.addSuppression)
        self.comboBox.currentIndexChanged.connect(self.addContent)
        self.button_propuesta.clicked.connect(self.propuesta)
    
    def setData(self, data):
        self.conjuntos.clear()
        self.comboBox.clear()
        if bd_attributes.exist():
            attributes = bd_attributes.getNonSensible()
        else:
            attributes = []

        for header in attributes:
            self.comboBox.addItem(header)
        
        for j in range(len(data[0])):
            conjunto = set()
            for i in range(len(data)):
                conjunto.add(data[i][j])
            self.conjuntos.append(conjunto)
        self.addContent()
    
    def addContent(self):
        for j in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
        attribute = self.comboBox.currentText()
        self.button_guardar.setText(f'Guardar datos de {attribute}')
        index = self.comboBox.currentIndex()

        i = 0
        if(self.conjuntos):
            for elto in self.conjuntos[index]:
                celda = QTableWidgetItem(str(elto))
                celda.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, celda)
                i = i+1

        if(bd_hierarchy.exist(attribute)):
            data = bd_hierarchy.getData(attribute)
            
            while(self.tableWidget.columnCount() < len(data[0])):
                self.addLevel()
            
            for i in range(len(data)):
                for j in range(1,len(data[0])):
                    celda = QTableWidgetItem(str(data[i][j]))
                    
                    self.tableWidget.setItem(i, j, celda)

    def addLevel(self):
        column = self.tableWidget.columnCount()
        self.tableWidget.insertColumn(column)
        item = QtWidgets.QTableWidgetItem(f'Nivel {column}')
        self.tableWidget.setHorizontalHeaderItem(column, item)

    def deleteLevel(self):
        column = self.tableWidget.columnCount()
        self.tableWidget.removeColumn(column-1)

    def createHierarchies(self):
        bd.dropAlgorithmData()

        attribute = self.comboBox.currentText()
                
        if(bd_hierarchy.exist(attribute)):
            bd_hierarchy.drop(attribute)
        
        columns = 0
        for j in range(self.tableWidget.columnCount()):
            if((str(type(self.tableWidget.item(0,j)))=="<class 'NoneType'>")==False):
                if(self.tableWidget.item(0,j).text()!=''):
                    columns = columns +1

        bd_hierarchy.create(attribute,columns)
        self.tableWidget.setColumnCount(columns)

        error = False
        for i in range(self.tableWidget.rowCount()):
            row = []
            for j in range(self.tableWidget.columnCount()):
                if((str(type(self.tableWidget.item(i,j)))=="<class 'NoneType'>")==False):
                    row.append(self.tableWidget.item(i,j).text())
            try:
                bd_hierarchy.insert(attribute, row)    
            except:
                error = True

        if(error):
            QMessageBox.about(self, "Error", "Ha ocurrido un error al guardar la jerarquía indicada")        
        else:
            QMessageBox.about(self, "Actualización correcta", "Se han actualizado correctamente los datos de la jerarquía de "+attribute)

    def importHierarchy(self):
        archivo = QFileDialog.getOpenFileName(self, 'Exportar datos', '~/Escritorio', "(*.csv *.txt)")
        if(len(archivo[0])>0):
            file = open(archivo[0], 'r')
            
            reader = csv.reader(file, delimiter=',')
            data = list(reader)

            while(self.tableWidget.columnCount() < len(data[0])):
                self.addLevel()
            
            for i in range(len(data)):
                for j in range(len(data[0])):
                    celda = QTableWidgetItem(str(data[i][j]))
                    
                    self.tableWidget.setItem(i, j, celda)

    def exportHierarchy(self):
        items = []
        for i in range(self.tableWidget.rowCount()):
            row = []
            for j in range(self.tableWidget.columnCount()):
                if((str(type(self.tableWidget.item(i,j)))=="<class 'NoneType'>")==False):
                    row.append(self.tableWidget.item(i,j).text())
            items.append(row)
        
        archivo = QFileDialog.getSaveFileName(self, 'Exportar datos', '~/Escritorio', "(*.csv *.txt)")
        if(len(archivo[0])>0):
            if('.' in archivo[0]):
                file = open(archivo[0], 'w')
            else:
                file = open(f'{archivo[0]}.csv', 'w')
            with file:
                writer = csv.writer(file)
                writer.writerows(items)
        
        QMessageBox.about(self, "Jerarquía exportada", f"La jerarquía ha sido guardada en {archivo[0]}")

    def addSuppression(self):
        added = False
        suppress = "*"
        pattern = re.compile("int")
        tipo = bd_data.getTypeColumn(self.comboBox.currentText())
        if(pattern.search(tipo)): 
            lon = int(tipo.split('(')[1].split(')')[0])
            for i in range(lon-1):
                suppress = suppress + "*"  
        
        for j in range(1, self.tableWidget.columnCount()):
            if(str(type(self.tableWidget.item(0,j)))=="<class 'NoneType'>"):
                for i in range(self.tableWidget.rowCount()):
                    self.tableWidget.setItem(i, self.tableWidget.columnCount()-1, QTableWidgetItem(suppress)) 
                added = True                       
        if(added==False):
            self.addLevel()
            for i in range(self.tableWidget.rowCount()):
                self.tableWidget.setItem(i, self.tableWidget.columnCount()-1, QTableWidgetItem(suppress))
        
    def propuesta(self):
        pattern = re.compile("int")
        type = bd_data.getTypeColumn(self.comboBox.currentText())
        if(pattern.search(type)): 
            lon = int(type.split('(')[1].split(')')[0])
            for i in range(self.tableWidget.columnCount(), lon):
                self.addLevel()
                
            for i in range(self.tableWidget.rowCount()):
                item = list(self.tableWidget.item(i, 0).text())
                for j in range(1, lon):
                    item[len(item)-j] = '*'
                    self.tableWidget.setItem(i,j,QTableWidgetItem("".join(item)))

            for i in range(1,self.tableWidget.columnCount()):
                items = []
                for j in range(self.tableWidget.rowCount()):
                    items.append(self.tableWidget.item(j,i).text())
                if(len(set(items))==1):
                    self.tableWidget.setColumnCount(i+1)
                    break
        else:
            QMessageBox.about(self, "Error", "Sólo se pueden generar propuestas de jerarquía para números")
            
class Results(QMainWindow, Ui_ResultsWindow): 
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.resize(width,height)
        self.button_layout = QGridLayout()
        self.button_group = QButtonGroup()
        self.groupBox.setLayout(self.button_layout)
        self.button_generalization.clicked.connect(self.applyGeneralization)
        self.button_export.clicked.connect(self.exportData)
        self.quasiidentifiers = []

    def setGeneralizations(self, generalizations):
        self.generalizations = generalizations
        while self.button_layout.count()>0: 
            self.button_layout.itemAt(0).widget().setParent(None)
        
        i = 1
        j = 1
        id = 0
        suma = 0
        for g in range(len(generalizations)):
            aux = 0
            for a in generalizations[g].getValue():
                aux = aux + a
            if g == 0:
                suma = aux
            if aux < suma:
                suma = aux    
        for g in generalizations:
            aux = 0
            for a in g.getValue():
                aux = aux + a
            radioButton = QRadioButton(str(g.getValue()))
            if (aux == suma):
                radioButton.setStyleSheet("color: red")
            self.button_layout.addWidget(radioButton, i, j)
            self.button_group.addButton(radioButton, id)
            j = j+1
            id = id+1
            if(j==4):
                i = i+1
                j = 1

    def setInitialData(self, headers, data, quasiidentifiers):
        self.groupBox.setTitle(f"Las generalizaciones candidatas para los atributos {quasiidentifiers} son:")
        nonSensible = bd_attributes.getNonIdentificator()
        self.data = list(bd_data.getDataByAttributes(nonSensible))
        new_data = []
        for row in data:
            aux = []
            for i in range(len(nonSensible)):
                aux.append(row[i])
            new_data.append(tuple(aux))
        self.setData(headers, tuple(new_data), quasiidentifiers)

    def setData(self, headers, data, quasiidentifiers):
        self.data = data
        self.headers = headers
        self.quasiidentifiers = quasiidentifiers
        model = TableModel.TableModel(data,headers)
        self.tableView.setModel(model)

    def applyGeneralization(self):
        generalization = self.generalizations[self.button_group.checkedId().numerator].getValue()
        nonIdentificator = bd_attributes.getNonIdentificator()
        data = list(bd_data.getDataByAttributes(nonIdentificator))

        new_data = []
        for row in data:
            aux = []
            gen = 0
            for i in range(len(nonIdentificator)):
                attribute = bd_attributes.getNameNonIdentificator(i)
                if(attribute in self.quasiidentifiers):
                    aux.append(bd_hierarchy.getGeneralization(attribute, 0, generalization[gen], row[i]))
                    gen = gen + 1
                else:
                    aux.append(row[i])
                
            new_data.append(tuple(aux))
    
        self.setData(self.headers, tuple(new_data), self.quasiidentifiers)

    def exportData(self):
        archivo = QFileDialog.getSaveFileName(self, 'Exportar datos', '~/Escritorio', "(*.csv *.txt)")
        if(len(archivo[0])>0):
            if('.' in archivo[0]):
                file = open(archivo[0], 'w')
            else:
                file = open(f'{archivo[0]}.csv', 'w')
            with file:
                writer = csv.writer(file)
                headers = [bd_attributes.getNonIdentificator()]
                writer.writerows(headers)
                writer.writerows(self.data)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    screen = app.primaryScreen()
    width = screen.size().width()
    height = screen.size().height()
    window = Table()
    app.exec_()
