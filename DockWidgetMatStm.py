from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pandas as pd
from functools import partial
from component_selector import *
from collections import defaultdict
from Graphics import *

ui_dialog,_ = loadUiType('DockWidgetMatStm.ui')

class DockWidgetMatStm(QDockWidget,ui_dialog):

    def __init__(self,name,comptype,obj,container,parent=None):
        QDockWidget.__init__(self,parent)
        self.setupUi(self)
        self.setWindowTitle(obj.name)
        self.name=name
        self.obj=obj
        self.type = comptype
        self.inputdict = {}
        self.x_pclist = []
        self.modes()
        self.comboBox.currentIndexChanged.connect(self.modeSelection)

        print("constructor ", self.inputdict)
        self.pushButton_2.clicked.connect(self.param)
        self.dict = {}

        self.nameType = None
        self.container = container

        header = QTreeWidgetItem(['Compound','Value','Unit'])
        self.mTreeWidget.setHeaderItem(header)
        self.lTreeWidget.setHeaderItem(header)
        self.vTreeWidget.setHeaderItem(header)       

        self.mTreeWidget.itemClicked.connect(lambda : self.printer(self.mTreeWidget.currentItem()))
        self.lTreeWidget.itemClicked.connect(lambda : self.printer(self.lTreeWidget.currentItem()))
        self.vTreeWidget.itemClicked.connect(lambda : self.printer(self.vTreeWidget.currentItem()))


    def printer(self, treeItem ):
	    foldername = treeItem.text(0)
	    comment = treeItem.text(1)
	    data = treeItem.text(2)
	    print(foldername , ': ' , comment , ' (' + data + ')')

    # input data tab
    def modes(self):
        modesList = self.obj.modesList
        if(modesList):
            for j in modesList:
                self.comboBox.addItem(str(j))
            self.modeSelection()
        else:
            self.inputdict= {}
            self.inputdict = self.obj.paramgetter()
            self.inputparamslist()

    def modeSelection(self):
        self.inputdict= {}
        for i in reversed(range(self.formLayout.count())):
            self.formLayout.removeRow(i) 
        self.inputdict = self.obj.paramgetter(self.comboBox.currentText())
        self.inputparamslist()

    def inputparamslist(self):
        try:
            print("inputparamslist ", self.inputdict)
            for c,i in enumerate(self.inputdict):
                if(i=="thermoPackage"):
                    print("thermo1")
                    combo = QComboBox()
                    self.lines = [line.rstrip('\n') for line in open('thermopackage.txt')]
                    print("thermo2")
                    for j in self.lines:
                        combo.addItem(str(j))
                    lay = QGridLayout()
                    lay.addWidget(QLabel(i+":"), 0,0, alignment=Qt.AlignLeft)
                    lay.addWidget(combo, 0, 1, alignment=Qt.AlignRight)
                    self.formLayout.addRow(lay)
                    self.inputdict[i] = combo   
                    print("thermo")
                elif(i=="condType"):
                    combo = QComboBox()
                    self.lines = ["Total","Partial"]
                    for j in self.lines:
                        combo.addItem(str(j))
                    lay = QGridLayout()
                    lay.addWidget(QLabel("Condensor Type :"+":"), 0, 0, alignment=Qt.AlignLeft)
                    lay.addWidget(combo, 0, 1, alignment=Qt.AlignCenter)
                    self.formLayout.addRow(lay)
                    self.inputdict[i] = combo
                elif(i=="x_pc"):
                    noc = len(compound_selected)
                    print(noc)
                    self.x_pclist.clear()
                    
                    gp = QGroupBox("Mole Fractions")
                    lay = QGridLayout()
                    for j in range(noc):
                        l = QLineEdit()  
                        if self.inputdict[i] != '':
                            l.setText(str(self.obj.variables[compound_selected[j]]['value']))
                        self.inputdict[i] = "x_pc"
                        lay.addWidget(QLabel(str(compound_selected[j])+":"),j,0, alignment=Qt.AlignLeft)
                        lay.addWidget(l,j,1, alignment=Qt.AlignCenter)
                        self.x_pclist.append(l)
                  
                    gp.setLayout(lay)
                    self.formLayout.addRow(gp)  
                else:
                    print("elseloop")
                    l = QLineEdit()
                    if self.inputdict[i] != None:
                        l.setText(str(self.inputdict[i]))
                    lay = QGridLayout()
                    lay.addWidget(QLabel(i+":"),0,0, alignment=Qt.AlignLeft)
                    lay.addWidget(l,0,1, alignment=Qt.AlignCenter)
                    if(i != 'MolFlow'):
                        lay.addWidget(QLabel(self.obj.variables[i]['unit']),0,2, alignment=Qt.AlignCenter)
                    else:
                        lay.addWidget(QLabel("mol/s"),0,2, alignment=Qt.AlignCenter)
                    self.formLayout.addRow(lay)
                    self.inputdict[i] = l
            
        except Exception as e:
            print(e)

    def Show_Error(self):
        QMessageBox.about(self, 'Important', "Please fill all fields with data")

    def param(self):
        try:
            self.dict={}

            print("param.inputdict ", self.inputdict)
            for i in self.inputdict:
                if(i=="thermoPackage"):
                    if (self.inputdict[i].currentText()):
                        self.dict[i] = self.inputdict[i].currentText()
                    else:
                        self.Show_Error()
                        break
                elif(i=="condType"):
                    if (self.inputdict[i].currentText()):
                        self.dict[i] = self.inputdict[i].currentText()
                    else:
                        self.Show_Error()
                        break
                elif(i =="x_pc"):
                    l=[]
                    mf = []
                    total_moles = 0
                    for mol_frac in self.x_pclist:
                        if (mol_frac.text()):
                            l.append(mol_frac.text())
                            total_moles += float(l[-1])
                        else:
                            self.Show_Error()
                            break
                    for c in range(len(compound_selected)):
                        mf.append(str(float(l[c])/total_moles))
                        self.obj.variables[compound_selected[c]]['value'] = str(float(l[c])/total_moles)
                        self.x_pclist[c].setText(mf[-1])
                    self.dict[i] = ",".join(mf)
                else:
                    if (self.inputdict[i].text()):
                        self.dict[i] = self.inputdict[i].text()
                    else:
                        print(self.inputdict[i].text())
                        self.Show_Error()
                        break
            
            print("param ", self.dict)
            self.obj.paramsetter(self.dict)
            self.hide()
            
        except Exception as e:
            print(e)


    @staticmethod
    def showResult(lst):
        #DockWidget1.flag = True
        for i in lst:
            i.resultsCategory(i.name)
            #i.show()
        
    # result data tab
    def resultsCategory(self,name):
        flag = True
        try:
            print("Under result category name ", name)
            result=self.container.result
            obj = self.container.fetchObject(name)

            d = {"Mole Fraction":"x_pc", "Mass Fraction":"xm_pc", "Mole Flow":"F_pc", "Mass Flow":"Fm_pc"}
            lst = list(d.keys())
            klst = list(d.values())

            p = {"Pressure":"P", "Temperature":"T","Vapour Phase Mole Fraction":"xvap", "Phase Molar Enthalpy":"H_p", 
            "Phase Molar Entropy":"S_p", "Molar Flow Rate":"F_p"}

            # Amounts Tab
            if obj.type == 'MaterialStream':
                l = []  # list for basis names
                for basis in d:
                    propertyname = name + '.' + d[basis]
                    print("basis ", basis, propertyname)
                    for i in result[0]:
                        if (propertyname in i):
                            l.append(i)
                print(l)
              
                j = 0
                t = 0
                namee = klst[j]
                print("namee ", namee)

                for i,k in enumerate(l):
                    ind = result[0].index(k)
                    print("index ", ind)
                    print("str ", k)
                    resultval = str(result[-1][ind])
                    print("######Resultsfetch####",resultval)
                    print(k[k.find(".")+1:k.find("[")])
                    obj.variables[k.split('.')[1]]['value'] = resultval
                    if namee in k:
                        if i%3 == 0: 
                            if(flag):                                  
                                mroot = QTreeWidgetItem(self.mTreeWidget, [lst[j]])
                            child = QTreeWidgetItem(mroot, [compound_selected[t], str(resultval),obj.variables[k.split('.')[1]]['unit']])
                        elif i%3 == 1:                                
                            if(flag):
                                lroot = QTreeWidgetItem(self.lTreeWidget, [lst[j]])
                            child = QTreeWidgetItem(lroot, [compound_selected[t], str(resultval),obj.variables[k.split('.')[1]]['unit']])
                        elif i%3 == 2:                                
                            if (flag):
                                vroot = QTreeWidgetItem(self.vTreeWidget, [lst[j]])
                            child = QTreeWidgetItem(vroot, [compound_selected[t], str(resultval),obj.variables[k.split('.')[1]]['unit']])
                            t += 1
                            flag = False
                    else:
                        j += 1
                        t = 0
                        namee = klst[j]
                        flag = True
                        if i%3 == 0:
                            if (flag):                                   
                                mroot = QTreeWidgetItem(self.mTreeWidget, [lst[j]])
                            child = QTreeWidgetItem(mroot, [compound_selected[t], str(resultval),obj.variables[k.split('.')[1]]['unit']])
                        elif i%3 == 1:                                
                            if (flag):
                                lroot = QTreeWidgetItem(self.lTreeWidget, [lst[j]])
                            child = QTreeWidgetItem(lroot, [compound_selected[t], str(resultval),obj.variables[k.split('.')[1]]['unit']])
                        elif i%3 == 2:                                
                            if (flag):
                                vroot = QTreeWidgetItem(self.vTreeWidget, [lst[j]])
                            child = QTreeWidgetItem(vroot, [compound_selected[t], str(resultval),obj.variables[k.split('.')[1]]['unit']])
                            t += 1
                            flag = False
                #print(obj.variables)
                
                # Phase Properties Tab
                phaseResLst = []
                for phase in p:
                    propertyname = name + '.' + p[phase]
                    print("phase ", phase, propertyname)
                    for i in result[0]:
                        if i.find('['):
                            if (propertyname == i[0:i.find('[')]):
                                phaseResLst.append(i)
                        if propertyname == i:
                            phaseResLst.append(i)
                print(phaseResLst)
                
                self.mTableWidget.setRowCount(0)
                self.lTableWidget.setRowCount(0)
                self.vTableWidget.setRowCount(0)

                for i,val in enumerate(phaseResLst):
                    ind = result[0].index(val)
                    resultval = str(result[-1][ind])
                    print(resultval, i, val)
                    obj.variables[val.split('.')[1]]['value'] = resultval
                    if '[' in val:
                        print(val)
                        temp = val[val.find('.')+1:val.find('[')]
                        print(temp)
                        if '1' in val.split('.')[1]:
                            print(obj.variables[val.split('.')[1]]['name'])
                            mrowPosition = self.mTableWidget.rowCount()
                            self.mTableWidget.insertRow(mrowPosition)
                            self.mTableWidget.setItem(mrowPosition , 0, QTableWidgetItem(obj.variables[val.split('.')[1]]['name']))
                            self.mTableWidget.setItem(mrowPosition , 1, QTableWidgetItem(resultval))
                            self.mTableWidget.setItem(mrowPosition , 2, QTableWidgetItem(obj.variables[val.split('.')[1]]['unit']))
                            self.mTableWidget.resizeColumnsToContents() 
                                                 
                        if '2' in val.split('.')[1]:       
                            lrowPosition = self.lTableWidget.rowCount()
                            self.lTableWidget.insertRow(lrowPosition)
                            self.lTableWidget.setItem(lrowPosition , 0, QTableWidgetItem(obj.variables[val.split('.')[1]]['name']))
                            self.lTableWidget.setItem(lrowPosition , 1, QTableWidgetItem(resultval))
                            self.lTableWidget.setItem(lrowPosition , 2, QTableWidgetItem(obj.variables[val.split('.')[1]]['unit']))
                            self.lTableWidget.resizeColumnsToContents()                         
                        if '3' in val.split('.')[1]:   
                            vrowPosition = self.vTableWidget.rowCount()
                            self.vTableWidget.insertRow(vrowPosition)
                            self.vTableWidget.setItem(vrowPosition , 0, QTableWidgetItem(obj.variables[val.split('.')[1]]['name']))
                            self.vTableWidget.setItem(vrowPosition , 1, QTableWidgetItem(resultval))
                            self.vTableWidget.setItem(vrowPosition , 2, QTableWidgetItem(obj.variables[val.split('.')[1]]['unit']))
                            self.vTableWidget.resizeColumnsToContents()                                
                    if not '[' in val:
                        #print(p[val.split('.')[1]])
                        print(obj.variables[val.split('.')[1]]['name'])
                        mrowPosition = self.mTableWidget.rowCount()
                        self.mTableWidget.insertRow(mrowPosition)
                        self.mTableWidget.setItem(mrowPosition , 0, QTableWidgetItem(obj.variables[val.split('.')[1]]['name']))
                        self.mTableWidget.setItem(mrowPosition , 1, QTableWidgetItem(resultval))
                        self.mTableWidget.setItem(mrowPosition , 2, QTableWidgetItem(obj.variables[val.split('.')[1]]['unit']))
                        self.mTableWidget.resizeColumnsToContents() 

            print(obj.variables)

        except Exception as e:
            print(e)
        

      