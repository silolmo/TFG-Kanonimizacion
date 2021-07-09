from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportDialog(object):
    def setupUi(self, ImportDialog):
        ImportDialog.setObjectName("ImportDialog")
        ImportDialog.resize(699, 439)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ImportDialog.sizePolicy().hasHeightForWidth())
        ImportDialog.setSizePolicy(sizePolicy)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(ImportDialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 10, 693, 421))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_types = QtWidgets.QGridLayout()
        self.gridLayout_types.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_types.setHorizontalSpacing(10)
        self.gridLayout_types.setVerticalSpacing(5)
        self.gridLayout_types.setObjectName("gridLayout_types")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setIndent(0)
        self.label_4.setObjectName("label_4")
        self.gridLayout_types.addWidget(self.label_4, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_types.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_types.addWidget(self.label_3, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_types)
        self.button_exportar = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_exportar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_exportar.setStyleSheet("background-color: rgb(243,217,176)")
        self.button_exportar.setObjectName("button_exportar")
        self.verticalLayout.addWidget(self.button_exportar)
        self.gridLayout_3.addLayout(self.verticalLayout, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem1, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 2, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.gridLayoutWidget_2)
        self.buttonBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 5, 0, 1, 3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem3, 3, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_data = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.edit_data.setInputMask("")
        self.edit_data.setObjectName("edit_data")
        self.horizontalLayout.addWidget(self.edit_data)
        self.button_openData = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_openData.setMinimumSize(QtCore.QSize(130, 0))
        self.button_openData.setMaximumSize(QtCore.QSize(130, 16777215))
        self.button_openData.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_openData.setStyleSheet("background-color: rgb(243,217,176)")
        self.button_openData.setObjectName("button_openData")
        self.horizontalLayout.addWidget(self.button_openData)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.label_data = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_data.setFont(font)
        self.label_data.setObjectName("label_data")
        self.gridLayout.addWidget(self.label_data, 0, 0, 1, 1)
        self.label_separator = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_separator.setFont(font)
        self.label_separator.setObjectName("label_separator")
        self.gridLayout.addWidget(self.label_separator, 1, 0, 1, 1)
        self.edit_separator = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.edit_separator.setObjectName("edit_separator")
        self.gridLayout.addWidget(self.edit_separator, 1, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setVerticalSpacing(20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_openAttributes = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_openAttributes.setMinimumSize(QtCore.QSize(130, 0))
        self.button_openAttributes.setMaximumSize(QtCore.QSize(130, 16777215))
        self.button_openAttributes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_openAttributes.setStyleSheet("background-color: rgb(243,217,176)")
        self.button_openAttributes.setObjectName("button_openAttributes")
        self.horizontalLayout_2.addWidget(self.button_openAttributes)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)
        self.button_addTypes = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.button_addTypes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_addTypes.setStyleSheet("background-color: rgb(233, 185, 110)")
        self.button_addTypes.setObjectName("button_addTypes")
        self.gridLayout_2.addWidget(self.button_addTypes, 1, 0, 1, 3)
        self.edit_attributes = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.edit_attributes.setObjectName("edit_attributes")
        self.gridLayout_2.addWidget(self.edit_attributes, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 2, 1, 1, 1)
        self.label_attributes = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_attributes.setFont(font)
        self.label_attributes.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_attributes.setObjectName("label_attributes")
        self.gridLayout.addWidget(self.label_attributes, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 3)

        self.retranslateUi(ImportDialog)
        self.buttonBox.accepted.connect(ImportDialog.accept)
        self.buttonBox.rejected.connect(ImportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportDialog)

    def retranslateUi(self, ImportDialog):
        _translate = QtCore.QCoreApplication.translate
        ImportDialog.setWindowTitle(_translate("ImportDialog", "Insertar datos"))
        self.label_4.setText(_translate("ImportDialog", "Longitud máxima"))
        self.label_2.setText(_translate("ImportDialog", "Atributos"))
        self.label_3.setText(_translate("ImportDialog", "Tipos"))
        self.button_exportar.setText(_translate("ImportDialog", "Exportar a un fichero"))
        self.button_openData.setText(_translate("ImportDialog", "Abrir fichero"))
        self.label_data.setText(_translate("ImportDialog", "Datos:"))
        self.label_separator.setText(_translate("ImportDialog", "Separador de los datos:"))
        self.button_openAttributes.setText(_translate("ImportDialog", "Abrir fichero"))
        self.button_addTypes.setText(_translate("ImportDialog", "Añadir manualmente"))
        self.label_attributes.setText(_translate("ImportDialog", "Tipos de los atributos:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImportDialog = QtWidgets.QDialog()
    ui = Ui_ImportDialog()
    ui.setupUi(ImportDialog)
    ImportDialog.show()
    sys.exit(app.exec_())
